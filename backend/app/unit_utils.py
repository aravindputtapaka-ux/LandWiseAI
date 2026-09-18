# Approximate conversions to square feet.
# Bigha is region-dependent; this default is only a placeholder and should
# be replaced with a location-specific conversion for production use.
UNIT_TO_SQFT = {
    "sq ft": 1,
    "sqft": 1,
    "sq yd": 9,
    "sqyd": 9,
    "gaj": 9,
    "sq m": 10.7639,
    "sqm": 10.7639,
    "cent": 435.6,
    "acre": 43560,
    "hectare": 107639,
    "marla": 272.25,
    "gunta": 1089,
    "bigha": 27225,
}


def normalize_unit(unit: str) -> str:
    value = unit.lower().strip()
    aliases = {
        "square feet": "sq ft",
        "square foot": "sq ft",
        "square yard": "sq yd",
        "square yards": "sq yd",
        "square meter": "sq m",
        "square meters": "sq m",
    }
    return aliases.get(value, value)


def to_sqft(value: float, unit: str) -> float:
    return value * UNIT_TO_SQFT.get(normalize_unit(unit), 1)


def from_sqft(value: float, unit: str) -> float:
    factor = UNIT_TO_SQFT.get(normalize_unit(unit), 1)
    return value / factor


def price_between_units(price: float, from_unit: str, to_unit: str) -> float:
    # price per from_unit -> price per to_unit
    from_factor = UNIT_TO_SQFT.get(normalize_unit(from_unit), 1)
    to_factor = UNIT_TO_SQFT.get(normalize_unit(to_unit), 1)
    return price * (to_factor / from_factor)


def build_equivalents(price_per_unit: float, source_unit: str) -> dict:
    return {
        "sq_ft": round(price_between_units(price_per_unit, source_unit, "sq ft"), 2),
        "sq_yd": round(price_between_units(price_per_unit, source_unit, "sq yd"), 2),
        "sq_m": round(price_between_units(price_per_unit, source_unit, "sq m"), 2),
        "acre": round(price_between_units(price_per_unit, source_unit, "acre"), 2),
        "hectare": round(price_between_units(price_per_unit, source_unit, "hectare"), 2),
        "cent": round(price_between_units(price_per_unit, source_unit, "cent"), 2),
        "gunta": round(price_between_units(price_per_unit, source_unit, "gunta"), 2),
    }