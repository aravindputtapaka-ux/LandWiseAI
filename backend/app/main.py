from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.models import AffordabilityRequest, AffordabilityResponse, PriceInfo, PropertyPriceRequest
from app.services import tavily_service, gemini_service
from app.services.tavily_service import TavilyServiceError
from app.services.gemini_service import GeminiServiceError
from app.unit_utils import to_sqft, build_equivalents

app = FastAPI(
    title="LandWise AI Property API",
    description="Worldwide land and residential/commercial property price estimation using Tavily web evidence and Gemini extraction.",
    version="3.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


async def _get_property_info(location: str, property_type: str = "land", bhk: str | None = None, status: str | None = None) -> dict:
    try:
        search_data = await tavily_service.search_property_prices(location, property_type, bhk, status)
        price_data = await gemini_service.extract_property_data(location, property_type, bhk, status, search_data)
    except TavilyServiceError as exc:
        raise HTTPException(status_code=502, detail=f"Search failed: {exc}")
    except GeminiServiceError as exc:
        raise HTTPException(status_code=502, detail=f"Price extraction failed: {exc}")

    try:
        ppu = float(price_data.get("price_per_unit") or 0)
    except (TypeError, ValueError):
        ppu = 0
    avg = price_data.get("average_price")
    try:
        avg = float(avg) if avg is not None else None
    except (TypeError, ValueError):
        avg = None
    if ppu <= 0 and (avg is None or avg <= 0):
        raise HTTPException(status_code=404, detail=f"No usable property-price evidence was extracted for '{location}'. Try a larger nearby locality.")
    if ppu <= 0 and avg:
        ppu = avg
        price_data["unit"] = "property"
    price_data["price_per_unit"] = ppu
    price_data["property_type"] = property_type
    price_data["bhk"] = bhk
    price_data["property_status"] = status
    price_data["sources"] = [r.get("url") for r in search_data.get("results", []) if r.get("url")]
    return price_data


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "message": "LandWise AI Property API is running.", "docs": "/docs"}


@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "service": "LandWise AI Property", "version": "3.0.0"}


@app.post("/property-price", response_model=PriceInfo, tags=["property-price"])
async def get_property_price(req: PropertyPriceRequest):
    if req.property_type not in {"land", "flat", "villa", "independent_house", "commercial"}:
        raise HTTPException(status_code=422, detail="Unsupported property type.")
    data = await _get_property_info(req.location, req.property_type, req.bhk, req.property_status)
    return PriceInfo(
        location=req.location,
        property_type=req.property_type,
        bhk=req.bhk,
        property_status=req.property_status,
        price_per_unit=data["price_per_unit"],
        unit=data.get("unit", "sq ft"),
        currency=data.get("currency", req.currency),
        source_summary=data.get("summary", "AI analysis completed."),
        sources=data["sources"],
        confidence=data.get("confidence"),
        average_price=data.get("average_price"),
        min_price=data.get("min_price"),
        max_price=data.get("max_price"),
        average_price_per_sqft=data.get("average_price_per_sqft"),
        typical_area_min=data.get("typical_area_min"),
        typical_area_max=data.get("typical_area_max"),
        sample_size=data.get("sample_size"),
        market_trend=data.get("market_trend"),
    )


@app.get("/land-price", response_model=PriceInfo, tags=["land-price"])
async def get_land_price(location: str = Query(..., min_length=2)):
    data = await _get_property_info(location, "land")
    return PriceInfo(location=location, property_type="land", price_per_unit=data["price_per_unit"], unit=data.get("unit", "sq ft"), currency=data.get("currency", "INR"), source_summary=data.get("summary", ""), sources=data["sources"], confidence=data.get("confidence"), average_price=data.get("average_price"), min_price=data.get("min_price"), max_price=data.get("max_price"), average_price_per_sqft=data.get("average_price_per_sqft"), typical_area_min=data.get("typical_area_min"), typical_area_max=data.get("typical_area_max"), sample_size=data.get("sample_size"), market_trend=data.get("market_trend"))


@app.post("/affordability", response_model=AffordabilityResponse, tags=["affordability"])
async def calculate_affordability(req: AffordabilityRequest):
    data = await _get_property_info(req.location, "land")
    source_currency = data.get("currency", req.currency)
    if source_currency != req.currency:
        raise HTTPException(status_code=422, detail=f"Land price evidence is in {source_currency}, but your budget is in {req.currency}. Use the same currency for this prototype.")
    price = float(data["price_per_unit"])
    unit = data.get("unit", "sq ft")
    affordable = req.budget / price
    sqft = to_sqft(affordable, unit) if unit != "property" else 0
    return AffordabilityResponse(location=req.location, budget=req.budget, currency=req.currency, price_per_unit=price, unit=unit, affordable_area=round(affordable, 4), affordable_area_unit=unit, equivalent={**build_equivalents(1.0, unit), "affordable_sq_ft": round(sqft, 2)}, notes=data.get("summary", ""), sources=data["sources"])
