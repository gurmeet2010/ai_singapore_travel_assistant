
import asyncio

from mcp import Client
from app.mcp.currency_server import mcp


async def main():

    async with Client(mcp) as client:

        print("Connected to MCP server")

        # Discover available tools
        tools_result = await client.list_tools()

        print("\nAvailable tools:")

        for tool in tools_result.tools:
            print(f"- {tool.name}")

        # Call currency MCP tool
        result = await client.call_tool(
            "convert_currency",
            {
                "from_currency": "INR",
                "to_currency": "SGD",
                "amount": 50000
            }
        )

        print("\nTool result:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())

