import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parents[2]


async def call_mcp_tool(
    module_name: str,
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", module_name],
        cwd=str(PROJECT_ROOT),
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)

            if getattr(result, "is_error", False):
                raise RuntimeError(f"MCP tool {tool_name} returned an error.")

            structured = getattr(result, "structuredContent", None)
            if structured is None:
                structured = getattr(result, "structured_content", None)

            if structured:
                return structured

            content = getattr(result, "content", [])
            text_parts = [
                item.text
                for item in content
                if getattr(item, "type", None) == "text"
            ]

            return {"text": "\n".join(text_parts)}
