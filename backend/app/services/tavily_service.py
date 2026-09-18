import os
import httpx

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_URL = "https://api.tavily.com/search"


class TavilyServiceError(Exception):
    pass


def build_property_query(location: str, property_type: str = "land", bhk: str | None = None, status: str | None = None) -> str:
    p = property_type.replace("_", " ")
    if property_type == "land":
        return (
            f"current land plot price rate per sq ft sq yard acre in {location} "
            f"2026 real estate land price listings"
        )
    bhk_part = f" {bhk}" if bhk else ""
    status_part = f" {status.replace('_', ' ')}" if status else ""
    return (
        f"current{bhk_part} {p} price in {location}{status_part} "
        f"2026 real estate listings average sale price price per sq ft "
        f"property price range recent listings"
    )


async def search_property_prices(location: str, property_type: str = "land", bhk: str | None = None, status: str | None = None) -> dict:
    if not TAVILY_API_KEY:
        raise TavilyServiceError("TAVILY_API_KEY is not set.")
    query = build_property_query(location, property_type, bhk, status)
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "max_results": 8,
    }
    async with httpx.AsyncClient(timeout=35) as client:
        try:
            response = await client.post(TAVILY_URL, json=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise TavilyServiceError(f"Tavily returned {exc.response.status_code}: {exc.response.text}")
        except httpx.RequestError as exc:
            raise TavilyServiceError(f"Could not reach Tavily: {exc}")
    data = response.json()
    if not data.get("results") and not data.get("answer"):
        raise TavilyServiceError(f"No web results found for '{location}'.")
    return data


async def search_land_prices(location: str) -> dict:
    return await search_property_prices(location, "land")
