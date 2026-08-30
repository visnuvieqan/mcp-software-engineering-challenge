"""Deterministic task verifier.

The verifier grades behavior, not source-code similarity to the golden patch.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    result = subprocess.run(
        ["python", "-m", "pytest", "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
    )

    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")

    if result.returncode == 0:
        print("\nVERIFICATION: PASS")
        print("All task-specific and regression tests passed.")
        return 0

    print("\nVERIFICATION: FAIL")
    print("At least one required behavior is still incorrect.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
