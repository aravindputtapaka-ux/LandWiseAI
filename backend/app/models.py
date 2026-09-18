from typing import List, Optional
from pydantic import BaseModel, Field


PROPERTY_TYPES = ["land", "flat", "villa", "independent_house", "commercial"]


class AffordabilityRequest(BaseModel):
    location: str = Field(..., min_length=2, example="Gachibowli, Hyderabad")
    budget: float = Field(..., gt=0, example=5000000)
    currency: str = Field("INR", min_length=3, max_length=3)


class PriceInfo(BaseModel):
    location: str
    property_type: str = "land"
    bhk: Optional[str] = None
    property_status: Optional[str] = None
    price_per_unit: float
    unit: str
    currency: str
    source_summary: str
    sources: List[str] = []
    confidence: Optional[str] = None
    average_price: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    average_price_per_sqft: Optional[float] = None
    typical_area_min: Optional[float] = None
    typical_area_max: Optional[float] = None
    sample_size: Optional[int] = None
    market_trend: Optional[str] = None


class PropertyPriceRequest(BaseModel):
    property_type: str = Field("land", description="land, flat, villa, independent_house, commercial")
    location: str = Field(..., min_length=2)
    bhk: Optional[str] = None
    area: Optional[float] = Field(None, gt=0)
    area_unit: Optional[str] = "sq ft"
    property_status: Optional[str] = None
    currency: str = Field("INR", min_length=3, max_length=3)


class AffordabilityResponse(BaseModel):
    location: str
    budget: float
    currency: str
    price_per_unit: float
    unit: str
    affordable_area: float
    affordable_area_unit: str
    equivalent: dict
    notes: str
    sources: List[str] = []
