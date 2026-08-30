"""A deterministic demonstration of an agent-like tool loop.

This script is intentionally not an LLM. It demonstrates the same tool sequence an
agent might perform so the project can be tested without requiring an API key.

It:
1. reads the issue,
2. searches for the shipping function,
3. runs tests,
4. applies the known minimal fix,
5. runs tests again,
6. writes a trace.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from repo_tools import edit_file, read_file, run_tests, search_code

ROOT = Path(__file__).resolve().parent
TRACE_FILE = ROOT / "traces" / "demo_run.json"


def log(trace, action, arguments, result):
    trace.append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "arguments": arguments,
            "result": result,
        }
    )


def main():
    trace = []

    issue = read_file("issue.md")
    log(trace, "read_file", {"path": "issue.md"}, issue)

    matches = search_code("calculate_shipping")
    log(trace, "search_code", {"query": "calculate_shipping"}, matches)

    before = run_tests()
    log(trace, "run_tests", {}, before)

    shipping = read_file("src/shipping.py")
    log(trace, "read_file", {"path": "src/shipping.py"}, shipping)

    edit_result = edit_file(
        "src/shipping.py",
        "if subtotal >= 100:",
        "if subtotal > 100:",
    )
    log(
        trace,
        "edit_file",
        {
            "path": "src/shipping.py",
            "old_text": "if subtotal >= 100:",
            "new_text": "if subtotal > 100:",
        },
        edit_result,
    )

    after = run_tests()
    log(trace, "run_tests", {}, after)

    TRACE_FILE.write_text(json.dumps(trace, indent=2), encoding="utf-8")

    print(f"Trace written to {TRACE_FILE.relative_to(ROOT)}")
    print("Before:", "PASS" if before["passed"] else "FAIL")
    print("After:", "PASS" if after["passed"] else "FAIL")


if __name__ == "__main__":
    main()
