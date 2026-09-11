import asyncio

from mcp import Client

from app.mcp.weather_server import mcp


async def main():

    # Connect MCP client to our MCP server
    async with Client(mcp) as client:

        print("Connected to MCP server")

        # Get available tools
        tools = await client.list_tools()

        print("\nAvailable tools:")

        for tool in tools.tools:
            print(f"- {tool.name}")

        # Call the weather tool
        result = await client.call_tool(
            "get_singapore_weather",
            {
                "city": "Singapore"
            }
        )

        print("\nTool result:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())