#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 曝光度測試腳本

把 ai-visibility-questions.txt 裡的 10 個問題，分別丟給 claude 與 agy，
收集回答、判斷有沒有提到「留佇 / liozu-stay.com」，輸出成檔案。

結果檔分兩種：
  * ai-visibility-results/<時間戳>/  ── 每次執行的完整回答（逐次獨立）
  * summary-<題庫版本>.csv           ── 共用累積檔，每次執行往後「追加」，
                                       每列帶 run 欄可辨識是哪一次。
                                       題庫改題目時把「題庫版本」+1，就會換一個新 csv。

用法（PowerShell / cmd 都可以）：
    python ask_ai_visibility.py                  # 兩個工具都跑，全部 10 題（平行 4 條）
    python ask_ai_visibility.py --jobs 8         # 平行條數調高，跑更快
    python ask_ai_visibility.py --jobs 1         # 改回一題一題循序跑
    python ask_ai_visibility.py --only claude    # 只跑 claude
    python ask_ai_visibility.py --limit 2        # 只跑前 2 題（試水溫用）
    python ask_ai_visibility.py --no-answers     # 只印 O/X，不把整段回答印在畫面上
    python ask_ai_visibility.py --dry-run        # 只印出會問什麼，不真的呼叫
    python ask_ai_visibility.py --timeout 600    # 每題逾時秒數（預設 300）
    python ask_ai_visibility.py --agy-yolo       # agy 卡在權限詢問時才加

重要：AI 一定要在「專案目錄以外的空資料夾」裡回答，否則它會直接打開
      src/data/content.zh.json 照著唸，測出來是假陽性。本腳本已自動處理
      （在系統暫存區開一個空的 sandbox，並封鎖 claude 的檔案讀取工具）。
"""

import argparse
import csv
import datetime as dt
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUESTIONS_FILE = ROOT / "ai-visibility-questions.txt"
RESULTS_ROOT = ROOT / "ai-visibility-results"

# 命中判斷用的關鍵字：只要回答裡出現就算命中，不管資料來源是官網還是訂房網
HIT_PATTERN = re.compile(r"留佇|liozu-stay|liozu", re.IGNORECASE)
RIVAL_PATTERN = re.compile(r"小滿宿|littlefull|Little Full", re.IGNORECASE)

SEP_WIDE = "=" * 58
SEP_THIN = "-" * 58

CSV_FIELDS = ["run", "tool", "question_no", "hit", "rival_mentioned", "seconds", "exit_code"]

PRINT_LOCK = threading.Lock()


def setup_console():
    """讓 PowerShell / cmd 能正常印出中文，不要炸 UnicodeEncodeError。"""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def parse_version(path):
    """
    讀題庫檔開頭的「題庫版本：vN」。
    同一個版本的歷次測試結果，會累積寫進同一個 summary-vN.csv。
    """
    m = re.search(r"題庫版本：\s*(\S+)", path.read_text(encoding="utf-8"))
    return m.group(1) if m else "unversioned"


def parse_questions(path):
    """
    從題庫 txt 抽出問題。
    規則：以「數字. 」開頭的行是題目起點，後續縮排行是同一題的續行，
          遇到空行或「預期：」就結束。
    """
    if not path.exists():
        sys.exit("錯誤：找不到題庫檔 {}".format(path))

    questions = []
    current = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        start = re.match(r"^ *\d+\.\s+(.*)$", raw)
        if start:
            if current:
                questions.append(current)
            current = start.group(1).strip()
            continue

        if current is None:
            continue

        if not raw.strip() or raw.lstrip().startswith("預期："):
            questions.append(current)
            current = None
            continue

        if raw.startswith(" "):          # 縮排 = 上一題的續行
            current += " " + raw.strip()
        else:                            # 頂格文字 = 題目結束
            questions.append(current)
            current = None

    if current:
        questions.append(current)

    return questions


def build_command(tool, question, timeout, agy_yolo):
    """組出各工具的非互動式提問指令（每題都是全新一輪，不延續對話）。"""
    exe = shutil.which(tool)
    if exe is None:
        raise FileNotFoundError(tool)

    if tool == "claude":
        return [
            exe, "-p", question,
            # 只留搜尋能力，封鎖檔案工具，避免它讀本地原始碼作答
            "--allowed-tools", "WebSearch", "WebFetch",
            "--disallowed-tools", "Read", "Glob", "Grep", "Bash", "Edit", "Write",
        ]

    if tool == "agy":
        cmd = [exe, "-p", question, "--print-timeout", "{}s".format(timeout)]
        if agy_yolo:
            cmd.append("--dangerously-skip-permissions")
        return cmd

    return [exe, "-p", question]


def ask(cmd, cwd, timeout):
    """執行一次提問，回傳 (回答, exit code, 耗時秒數)。"""
    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            timeout=timeout,
        )
        answer = (proc.stdout + proc.stderr).decode("utf-8", errors="replace").strip()
        code = proc.returncode
    except subprocess.TimeoutExpired as exc:
        partial = b""
        for chunk in (exc.stdout, exc.stderr):
            if chunk:
                partial += chunk
        answer = "(逾時 {}s，無完整回應)\n".format(timeout) + partial.decode("utf-8", errors="replace")
        code = 124
    return answer, code, int(time.monotonic() - start)


def run_job(job, sandbox, timeout, agy_yolo, progress, show_answer=True):
    """一個 (工具, 題號) 的完整工作：提問 → 判定命中 → 立刻印出 → 回傳結果。"""
    tool, no, question = job

    cmd = build_command(tool, question, timeout, agy_yolo)
    answer, code, elapsed = ask(cmd, sandbox, timeout)

    hit = "O" if HIT_PATTERN.search(answer) else "X"
    rival = "Y" if RIVAL_PATTERN.search(answer) else "N"

    # 一拿到答案就印。整段包在同一個 lock 裡，
    # 平行時各題的輸出才不會互相插隊變成亂碼。
    with PRINT_LOCK:
        progress["done"] += 1
        headline = "[{}/{}] {:<7} 第 {:>2} 題 ... {}（{}s）".format(
            progress["done"], progress["total"], tool, no, hit, elapsed)
        if show_answer:
            print("\n" + SEP_WIDE)
            print(headline + " ｜ 提到競品：{} ｜ exit={}".format(rival, code))
            print(SEP_WIDE)
            print("Q: " + question)
            print("\nA:")
            print(answer)
            print(SEP_THIN, flush=True)
        else:
            print(headline, flush=True)

    return {
        "tool": tool,
        "question_no": no,
        "question": question,
        "answer": answer,
        "hit": hit,
        "rival_mentioned": rival,
        "seconds": elapsed,
        "exit_code": code,
    }


def format_block(row):
    return (
        "{sep}\n"
        "第 {no} 題 ｜ 命中：{hit} ｜ 提到競品：{rival} ｜ 耗時：{sec}s ｜ exit={code}\n"
        "{sep}\n"
        "Q: {q}\n\nA:\n{a}\n\n"
    ).format(sep=SEP_THIN, no=row["question_no"], hit=row["hit"],
             rival=row["rival_mentioned"], sec=row["seconds"],
             code=row["exit_code"], q=row["question"], a=row["answer"])


def append_summary(rows, csv_path):
    """
    把這次的結果「追加」到共用的 summary-<版本>.csv。
    每列都帶 run 欄（執行時間戳），所以同一份題庫的歷次結果會累積在同一個檔案裡，
    可以直接排序、樞紐分析看趨勢。
    """
    is_new = not csv_path.exists()
    # 新檔用 utf-8-sig（Excel 開中文才不亂碼），既有檔用 utf-8 續寫，避免重複塞 BOM
    encoding = "utf-8-sig" if is_new else "utf-8"
    with open(csv_path, "a", encoding=encoding, newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
        if is_new:
            writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: (r["tool"], r["question_no"])))


def write_outputs(rows, tools, total, outdir, sandbox, questions_file, started, csv_path, version):
    """把平行跑完的結果依「工具 → 題號」排好序寫成檔案。"""
    combined_path = outdir / "all-answers.txt"
    done_tools = [t for t in tools if any(r["tool"] == t for r in rows)]

    combined = open(combined_path, "w", encoding="utf-8", newline="\n")
    combined.write("\n".join([
        "AI 曝光度測試結果",
        "執行時間：{:%Y-%m-%d %H:%M:%S}".format(started),
        "題庫：{}（版本 {}，共 {} 題）".format(questions_file, version, total),
        "工具：{}".format(" ".join(done_tools)),
        "作答目錄（沙箱）：{}".format(sandbox),
        "命中判斷：回答中出現 /{}/ 視為命中".format(HIT_PATTERN.pattern),
        "",
        "",
    ]))

    for tool in done_tools:
        tool_rows = sorted((r for r in rows if r["tool"] == tool),
                           key=lambda r: r["question_no"])
        hits = sum(1 for r in tool_rows if r["hit"] == "O")

        with open(outdir / "answers-{}.txt".format(tool), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("{}\n {} 的回答（{:%Y-%m-%d %H:%M:%S}）\n{}\n\n".format(
                SEP_WIDE, tool, started, SEP_WIDE))
            for row in tool_rows:
                block = format_block(row)
                fh.write(block)
                combined.write(block)
            fh.write("小計：命中 {}/{} 題\n".format(hits, total))

    lookup = {(r["question_no"], r["tool"]): r["hit"] for r in rows}
    table = [
        SEP_WIDE,
        " 總表（O = 有提到留佇／liozu-stay.com，X = 沒提到）",
        SEP_WIDE,
        "Q#".ljust(6) + "".join(t.ljust(10) for t in done_tools),
    ]
    for no in range(1, total + 1):
        table.append(
            str(no).ljust(6) + "".join(lookup.get((no, t), "-").ljust(10) for t in done_tools)
        )
    table.append("")
    for tool in done_tools:
        hits = sum(1 for r in rows if r["tool"] == tool and r["hit"] == "O")
        table.append("{}：命中 {}/{} 題".format(tool, hits, total))
    table.append("")
    table.append("明細（{} 全部歷次結果）：{}".format(version, csv_path.name))

    report = "\n".join(table)
    combined.write(report + "\n")
    combined.close()

    return report, combined_path, done_tools


def main():
    setup_console()

    parser = argparse.ArgumentParser(
        description="把題庫問題丟給 claude 與 agy，收集回答並判斷是否提到留佇。",
    )
    parser.add_argument("--only", metavar="TOOL", help="只跑指定的工具（claude 或 agy）")
    parser.add_argument("--limit", type=int, default=0, metavar="N", help="只跑前 N 題")
    parser.add_argument("--jobs", "-j", type=int, default=4, metavar="N",
                        help="同時平行幾條（預設 4；設 1 就是循序跑）")
    parser.add_argument("--no-answers", action="store_true",
                        help="只印命中結果，不要把整段回答印在畫面上")
    parser.add_argument("--dry-run", action="store_true", help="只印出會問什麼，不真的呼叫")
    parser.add_argument("--timeout", type=int, default=300, metavar="SEC",
                        help="每題逾時秒數（預設 300）")
    parser.add_argument("--agy-yolo", action="store_true", help="讓 agy 自動核准工具權限")
    parser.add_argument("--questions", type=Path, default=QUESTIONS_FILE, help="題庫檔路徑")
    parser.add_argument("--outdir", type=Path, default=None, help="輸出目錄")
    parser.add_argument("--summary", type=Path, default=None,
                        help="共用結果 CSV 路徑（預設 summary-<題庫版本>.csv）")
    args = parser.parse_args()

    tools = [args.only] if args.only else ["claude", "agy"]

    version = parse_version(args.questions)
    csv_path = args.summary or (ROOT / "summary-{}.csv".format(version))

    questions = parse_questions(args.questions)
    if not questions:
        sys.exit("錯誤：從 {} 讀不到任何問題".format(args.questions))
    if len(questions) != 10:
        print("警告：預期 10 題，實際讀到 {} 題（題庫格式可能被改過）".format(len(questions)),
              file=sys.stderr)
    if 0 < args.limit < len(questions):
        questions = questions[:args.limit]
    total = len(questions)

    if args.dry_run:
        print("(dry-run) 共 {} 題 × {} 個工具 = {} 次提問\n".format(
            total, len(tools), total * len(tools)))
        for tool in tools:
            for no, question in enumerate(questions, 1):
                print("[{}] 第 {}/{} 題 ... {}".format(tool, no, total, question))
        print("\n(dry-run 結束，未產生結果檔)")
        return 0

    # 先確認工具存在，不存在的直接剔除
    available = []
    for tool in tools:
        if shutil.which(tool) is None:
            print("!! 找不到指令 '{}'，略過".format(tool), file=sys.stderr)
        else:
            available.append(tool)
    if not available:
        sys.exit("錯誤：沒有任何可用的工具")

    started = dt.datetime.now()
    run_id = started.strftime("%Y%m%d-%H%M%S")
    outdir = args.outdir or (RESULTS_ROOT / run_id)
    outdir.mkdir(parents=True, exist_ok=True)

    # AI 作答用的中立空目錄：絕對不能是本專案
    sandbox = Path(tempfile.gettempdir()) / "ai-visibility-sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)

    jobs = [(tool, no, q)
            for tool in available
            for no, q in enumerate(questions, 1)]
    workers = max(1, min(args.jobs, len(jobs)))
    progress = {"done": 0, "total": len(jobs)}

    print("題庫版本：{}　｜　累積結果：{}".format(version, csv_path))
    print("輸出目錄：{}".format(outdir))
    print("共 {} 題 × {} 個工具 = {} 次提問，平行 {} 條\n".format(
        total, len(available), len(jobs), workers))

    rows = []
    wall_start = time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(run_job, job, sandbox, args.timeout, args.agy_yolo,
                               progress, not args.no_answers)
                   for job in jobs]
        for future in as_completed(futures):
            try:
                rows.append(future.result())
            except Exception as exc:  # 單題爆掉不要拖垮整批
                with PRINT_LOCK:
                    print("!! 有一題執行失敗：{}".format(exc), file=sys.stderr)
    wall = int(time.monotonic() - wall_start)

    if not rows:
        sys.exit("錯誤：沒有任何題目成功執行")

    for row in rows:
        row["run"] = run_id
    append_summary(rows, csv_path)

    report, combined_path, done_tools = write_outputs(
        rows, available, total, outdir, sandbox, args.questions, started, csv_path, version)

    print()
    print(report)
    print("\n總耗時 {} 分 {} 秒".format(wall // 60, wall % 60))
    print("\n完成。結果檔：")
    print("  {}".format(combined_path))
    for tool in done_tools:
        print("  {}".format(outdir / "answers-{}.txt".format(tool)))
    print("  {}（{} 歷次累積，本次追加 {} 列）".format(csv_path, version, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
