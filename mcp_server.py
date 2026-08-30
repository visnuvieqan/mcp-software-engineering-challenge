"""MCP server exposing bounded software-engineering tools."""

from mcp.server.fastmcp import FastMCP

from repo_tools import (
    edit_file as _edit_file,
    list_files as _list_files,
    read_file as _read_file,
    run_tests as _run_tests,
    search_code as _search_code,
)

mcp = FastMCP("software-engineering-challenge")


@mcp.tool()
def list_files() -> list[str]:
    """List files available in the challenge repository."""
    return _list_files()


@mcp.tool()
def read_file(path: str) -> str:
    """Read a UTF-8 text file from the repository."""
    return _read_file(path)


@mcp.tool()
def search_code(query: str) -> list[dict[str, object]]:
    """Search repository text files for a case-insensitive query."""
    return _search_code(query)


@mcp.tool()
def edit_file(path: str, old_text: str, new_text: str) -> str:
    """Replace one exact text occurrence in a repository file."""
    return _edit_file(path, old_text, new_text)


@mcp.tool()
def run_tests() -> dict[str, object]:
    """Run the deterministic pytest verification suite."""
    return _run_tests()


if __name__ == "__main__":
    mcp.run()
