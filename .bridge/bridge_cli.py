#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / ".bridge"
REQUESTS = BRIDGE / "requests"
REPORTS = BRIDGE / "reports"
PROTOCOL = BRIDGE / "protocol.json"

def load(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def requests():
    out = []
    for path in sorted(REQUESTS.glob("*.json")):
        item = load(path)
        if "task_id" not in item or "protocol_version" not in item:
            raise SystemExit(f"Invalid request schema: {path}")
        out.append((path, item))
    return out

def report_path(task_id: str) -> Path:
    return REPORTS / f"{task_id}.json"

def pending():
    return [(p, r) for p, r in requests() if not report_path(r["task_id"]).exists()]

def cmd_status():
    protocol = load(PROTOCOL)
    reqs = requests()
    pend = pending()
    print(f"protocol={protocol['protocol_version']}")
    print(f"requests={len(reqs)}")
    print(f"pending={len(pend)}")
    print(f"reports={len(list(REPORTS.glob('*.json'))) if REPORTS.exists() else 0}")
    for _, r in pend:
        print(f"queued={r['task_id']}")

def cmd_next():
    pend = pending()
    if not pend:
        print("NO_PENDING_REQUESTS")
        return
    _, req = pend[0]
    print(json.dumps(req, indent=2, sort_keys=True))

def cmd_verify_report(task_id: str):
    path = report_path(task_id)
    if not path.exists():
        raise SystemExit(f"Missing report: {path}")
    report = load(path)
    if report.get("task_id") != task_id:
        raise SystemExit("Report task_id mismatch")
    if report.get("protocol_version") != "0.2":
        raise SystemExit("Report protocol_version mismatch")
    if report.get("status") not in {"blocked", "complete"}:
        raise SystemExit("Report status must be blocked or complete")
    print(f"REPORT_OK {task_id}")

def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "status"
    if command == "status":
        cmd_status()
    elif command == "next":
        cmd_next()
    elif command == "verify-report":
        if len(sys.argv) != 3:
            raise SystemExit("usage: bridge_cli.py verify-report TASK_ID")
        cmd_verify_report(sys.argv[2])
    else:
        raise SystemExit(f"unknown command: {command}")

if __name__ == "__main__":
    main()
