import re
from typing import Any

from app.mcp.client import call_mcp_tool


async def get_weather(forecast_days: int = 3) -> dict[str, Any]:
    return await call_mcp_tool(
        "app.mcp.weather_server",
        "get_singapore_weather",
        {"forecast_days": forecast_days},
    )


async def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict[str, Any]:
    return await call_mcp_tool(
        "app.mcp.currency_server",
        "convert_currency",
        {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
        },
    )


def extract_currency_request(question: str) -> tuple[float, str, str] | None:
    q = question.upper().strip()

    currency_pattern = r"(INR|USD|SGD|EUR)"

    # Find amount
    amount_match = re.search(
        r"(?:₹\s*)?([\d,]+(?:\.\d+)?)",
        q,
    )

    if not amount_match:
        return None

    amount = float(amount_match.group(1).replace(",", ""))

    # Find currencies
    currency_matches = list(
        re.finditer(currency_pattern, q)
    )

    if len(currency_matches) < 2:
        return None

    from_currency = currency_matches[0].group(1)
    to_currency = currency_matches[1].group(1)

    return amount, from_currency, to_currency
