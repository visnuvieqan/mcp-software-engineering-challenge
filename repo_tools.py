"""Bounded repository tools used by the MCP server.

These tools intentionally expose a small surface area suitable for a coding agent.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IGNORED_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache"}


def _safe_path(relative_path: str) -> Path:
    candidate = (ROOT / relative_path).resolve()
    if ROOT not in candidate.parents and candidate != ROOT:
        raise ValueError("path traversal outside repository is not allowed")
    return candidate


def list_files() -> list[str]:
    result: list[str] = []
    for path in ROOT.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file():
            result.append(str(path.relative_to(ROOT)))
    return sorted(result)


def read_file(path: str) -> str:
    target = _safe_path(path)
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(path)
    return target.read_text(encoding="utf-8")


def search_code(query: str) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    q = query.lower()

    for relative in list_files():
        if not relative.endswith((".py", ".md", ".json", ".txt")):
            continue

        text = read_file(relative)
        for line_no, line in enumerate(text.splitlines(), start=1):
            if q in line.lower():
                matches.append(
                    {"path": relative, "line": line_no, "text": line.strip()}
                )

    return matches[:100]


def edit_file(path: str, old_text: str, new_text: str) -> str:
    target = _safe_path(path)
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(path)

    content = target.read_text(encoding="utf-8")
    count = content.count(old_text)

    if count == 0:
        raise ValueError("old_text was not found")
    if count > 1:
        raise ValueError(
            "old_text matched more than once; provide a more specific edit"
        )

    target.write_text(content.replace(old_text, new_text, 1), encoding="utf-8")
    return f"updated {path}"


def run_tests() -> dict[str, object]:
    completed = subprocess.run(
        ["python", "-m", "pytest", "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
    )

    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "passed": completed.returncode == 0,
    }
