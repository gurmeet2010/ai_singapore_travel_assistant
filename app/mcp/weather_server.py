from datetime import date, timedelta

import httpx
#from mcp.server.fastmcp import FastMCP
from mcp.server.mcpserver import MCPServer


mcp = MCPServer("Singapore Weather MCP")


@mcp.tool()
async def get_singapore_weather(
    forecast_days: int = 3,
) -> dict:
    """Get current conditions and a forecast for Singapore from Open-Meteo."""
    if forecast_days < 1 or forecast_days > 7:
        raise ValueError("forecast_days must be between 1 and 7.")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 1.3521,
        "longitude": 103.8198,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum",
        "forecast_days": forecast_days,
        "timezone": "Asia/Singapore",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    daily = []
    for i, day in enumerate(data["daily"]["time"]):
        daily.append(
            {
                "date": day,
                "weather_code": data["daily"]["weather_code"][i],
                "temperature_max_c": data["daily"]["temperature_2m_max"][i],
                "temperature_min_c": data["daily"]["temperature_2m_min"][i],
                "precipitation_probability_percent": data["daily"]["precipitation_probability_max"][i],
                "precipitation_mm": data["daily"]["precipitation_sum"][i],
            }
        )

    return {
        "provider": "Open-Meteo",
        "location": "Singapore",
        "retrieved_as_current_external_data": True,
        "current": data.get("current", {}),
        "daily": daily,
    }


if __name__ == "__main__":
    mcp.run()
