# MCP Software Engineering Challenge Environment

A small, reproducible portfolio project that demonstrates four skills:

1. **MCP understanding & practical experience**
2. **Agentic AI engineering**
3. **Tool integration & agent debugging**
4. **Reproducible software-engineering tasks & verification**

The project contains a deliberately buggy Python function and an MCP server that exposes safe repository tools to an AI agent:

- `list_files`
- `read_file`
- `search_code`
- `edit_file`
- `run_tests`

The task is to fix the bug described in `issue.md` while preserving existing behavior.

## Challenge

The shipping rule is:

- Orders **over $100** receive free shipping.
- Orders **$100 or below** pay $10 shipping.

The starter implementation is intentionally wrong.

## Project structure

```text
mcp-software-engineering-challenge/
├── issue.md
├── task_manifest.json
├── golden_solution.patch
├── verifier.py
├── mcp_server.py
├── repo_tools.py
├── simulate_agent.py
├── requirements.txt
├── Dockerfile
├── src/
│   ├── __init__.py
│   └── shipping.py
├── tests/
│   └── test_shipping.py
└── traces/
    └── example_trace.json
```

## Why this is useful

The environment is deterministic and easy to verify:

- The repository state is fixed.
- Tests define expected behavior.
- The verifier checks both the new behavior and regressions.
- The MCP server exposes only bounded repository operations.
- A golden patch proves the task is solvable.
- A trace example shows how tool calls can be inspected during debugging.

## Local setup

Python 3.11+ recommended.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Run the tests:

```bash
pytest -q
```

The starter repo should fail one task-specific test.

Run the verifier:

```bash
python verifier.py
```

Run the MCP server:

```bash
python mcp_server.py
```

The server uses the Python MCP SDK and exposes repository tools over the default transport.

## Agent task

Give an MCP-capable coding agent this instruction:

> Read `issue.md`, inspect the repository, fix the bug using the available tools, and run the test suite. Stop only when all tests pass.

## Verification philosophy

The evaluator does **not** compare the candidate implementation to the golden patch. It verifies behavior.

That allows many correct implementations, for example:

```python
def calculate_shipping(total):
    if total > 100:
        return 0
    return 10
```

or:

```python
def calculate_shipping(total):
    return 0 if total > 100 else 10
```

Both pass because they satisfy the same behavior.

## Fail-to-pass vs pass-to-pass

The test suite includes:

- **Fail-to-pass:** the deliberately failing free-shipping behavior.
- **Pass-to-pass:** existing shipping behavior that must remain correct.

This is important for agent evaluation: the agent must fix the target bug without causing regressions.

## Safety notes

`repo_tools.py` restricts file access to this repository directory and blocks path traversal outside it.

For production environments, add:
- authorization,
- stronger sandboxing,
- rate limits,
- idempotency protections for side-effecting tools,
- structured tracing,
- resource quotas,
- and a container-per-task execution model.

## Portfolio talking points

When discussing this project in an interview:

- Explain MCP as the standardized tool interface between an AI host/client and external capabilities.
- Explain why tool schemas and bounded permissions matter.
- Show how a trace isolates failures across tool selection, arguments, execution, and interpretation.
- Explain why reproducible tasks need pinned inputs, deterministic tests, and explicit verification.
- Explain why a golden solution proves solvability but should not be the grading target.
