import httpx
from mcp.server.mcpserver import MCPServer


mcp = MCPServer("Currency Conversion MCP")


@mcp.tool()
async def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    """Convert an amount using the latest rate returned by Frankfurter."""
    if amount < 0:
        raise ValueError("amount must be non-negative.")

    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    if len(from_currency) != 3 or len(to_currency) != 3:
        raise ValueError("Currencies must be ISO 4217 three-letter codes.")

    if from_currency == to_currency:
        return {
            "provider": "Frankfurter",
            "from": from_currency,
            "to": to_currency,
            "amount": amount,
            "rate": 1.0,
            "converted_amount": amount,
        }

    url = "https://api.frankfurter.dev/v1/latest"
    params = {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    converted = data["rates"][to_currency]
    rate = converted / amount if amount else 0.0

    return {
        "provider": "Frankfurter",
        "date": data.get("date"),
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "rate": rate,
        "converted_amount": converted,
    }


if __name__ == "__main__":
    mcp.run()
