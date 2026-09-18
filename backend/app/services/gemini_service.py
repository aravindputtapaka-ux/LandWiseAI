import json
import os
import httpx

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


class GeminiServiceError(Exception):
    pass


def _context(search_data: dict) -> str:
    parts = []
    if search_data.get("answer"):
        parts.append(f"Search summary: {search_data['answer']}")
    for i, result in enumerate(search_data.get("results", []), 1):
        parts.append(f"[Source {i}] {result.get('title', '')}\nURL: {result.get('url', '')}\nExcerpt: {result.get('content', '')}")
    return "\n\n".join(parts)[:18000]


async def extract_property_data(location: str, property_type: str, bhk: str | None, status: str | None, search_data: dict) -> dict:
    if not GEMINI_API_KEY:
        raise GeminiServiceError("GEMINI_API_KEY is not set.")
    prompt = f"""
You are extracting current real-estate pricing from web evidence.

LOCATION: {location}
PROPERTY TYPE: {property_type}
BHK: {bhk or 'not specified'}
STATUS: {status or 'not specified'}

WEB EVIDENCE:
{_context(search_data)}

Return ONLY valid JSON:
{{
  "price_per_unit": number,
  "unit": "sq ft|sq yd|sq m|acre|cent|gunta|hectare|marla|bigha|property",
  "currency": "3-letter currency code",
  "average_price": number or null,
  "min_price": number or null,
  "max_price": number or null,
  "average_price_per_sqft": number or null,
  "typical_area_min": number or null,
  "typical_area_max": number or null,
  "sample_size": integer or null,
  "market_trend": "short factual description or null",
  "confidence": "low|medium|high",
  "summary": "1-3 concise sentences"
}}

Rules:
- Use only evidence in the supplied web results.
- For flats, villas and houses, price_per_unit should normally be the price per sq ft when evidence supports it.
- average_price is the typical asking/sale price for the requested property configuration (including BHK when supplied).
- For land, use a land-area unit such as sq ft, sq yd or acre.
- If multiple values conflict, use a reasonable typical value and lower confidence.
- Asking prices are not guaranteed transaction prices; mention uncertainty briefly when appropriate.
- Do not invent missing values. Use null or 0 where no usable evidence exists.
"""
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}}
    async with httpx.AsyncClient(timeout=45) as client:
        try:
            response = await client.post(GEMINI_URL, params={"key": GEMINI_API_KEY}, headers={"Content-Type": "application/json"}, json=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise GeminiServiceError(f"Gemini returned {exc.response.status_code}: {exc.response.text}")
        except httpx.RequestError as exc:
            raise GeminiServiceError(f"Could not reach Gemini: {exc}")
    try:
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        return json.loads(text)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise GeminiServiceError(f"Invalid Gemini response: {exc}")


async def extract_price_data(location: str, search_data: dict) -> dict:
    return await extract_property_data(location, "land", None, None, search_data)
