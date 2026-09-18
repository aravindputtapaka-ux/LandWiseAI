# 🏡 LandWise AI --- Property Price Intelligence

LandWise AI is an AI-powered real-estate price intelligence application
that helps users research and estimate current property prices using
**real-time web evidence**.

The application started as a land/plot price estimation tool and has
been enhanced into a broader property intelligence platform supporting:

-   🌳 Land / Plot
-   🏢 Flat / Apartment
-   🏡 Villa
-   🏠 Independent House
-   🏬 Commercial Property

It combines a **React + TypeScript frontend**, **FastAPI backend**,
**Tavily web search**, and **Google Gemini** to retrieve current web
evidence, extract structured property-price information, and present the
results through a compact dashboard.

> **Important:** LandWise AI provides research-based estimates. Property
> listing prices are often asking prices rather than final transaction
> prices, and coverage varies by location. Results should not be treated
> as an official property valuation, appraisal, legal opinion, or
> guaranteed market price.

------------------------------------------------------------------------

## 📌 Table of Contents

-   [Project Overview](#-project-overview)
-   [Why LandWise AI](#-why-landwise-ai)
-   [Use Cases](#-use-cases)
-   [Supported Property Types](#-supported-property-types)
-   [Core Features](#-core-features)
-   [Price Analysis](#-price-analysis)
-   [Affordability Analysis](#-affordability-analysis)
-   [Dynamic BHK Logic](#-dynamic-bhk-logic)
-   [Commercial Property Logic](#-commercial-property-logic)
-   [City and Locality Analysis](#-city-and-locality-analysis)
-   [How the AI Pipeline Works](#-how-the-ai-pipeline-works)
-   [System Architecture](#-system-architecture)
-   [Technology Stack](#-technology-stack)
-   [Project Structure](#-project-structure)
-   [Frontend](#-frontend)
-   [Backend](#-backend)
-   [API Endpoints](#-api-endpoints)
-   [Request Examples](#-request-examples)
-   [Environment Variables](#-environment-variables)
-   [Installation](#-installation)
-   [Running the Application](#-running-the-application)
-   [Production Frontend Build](#-production-frontend-build)
-   [Location Search](#-location-search)
-   [Gemini Reliability and Retry
    Handling](#-gemini-reliability-and-retry-handling)
-   [Error Handling](#-error-handling)
-   [Data and Pricing Methodology](#-data-and-pricing-methodology)
-   [Security](#-security)
-   [Limitations](#-limitations)
-   [Future Enhancements](#-future-enhancements)
-   [Troubleshooting](#-troubleshooting)
-   [Development Workflow](#-development-workflow)
-   [License](#-license)

------------------------------------------------------------------------

# 🚀 Project Overview

LandWise AI is designed for users who want to answer questions such as:

> "What is the current estimated price of a 2 BHK flat in Gachibowli?"

> "What is the average 3 BHK villa price in Hyderabad?"

> "What areas of Hyderabad can I consider with a ₹80 lakh budget?"

> "What is the current price of land in a particular locality?"

> "How much does a commercial shop cost in a selected area?"

Instead of relying on a single static database value, the application
searches the web for current evidence and uses Gemini to convert the
retrieved information into structured property-price data.

------------------------------------------------------------------------

# 🎯 Why LandWise AI

Traditional property-price applications often depend on:

-   Static datasets
-   Manually maintained prices
-   A single average value
-   City-level averages that ignore locality differences

LandWise AI takes a web-evidence approach:

``` text
User Input
    ↓
Property Type + Location + Requirements
    ↓
Tavily Web Search
    ↓
Current Property Evidence
    ↓
Gemini AI Extraction
    ↓
Structured Price Information
    ↓
Price / Range / Market Information
    ↓
Dashboard Result
```

For affordability analysis, the system additionally searches for
locality-level evidence so that a city can be broken into recognizable
areas.

------------------------------------------------------------------------

# 💡 Use Cases

## 1. Land / Plot Price Research

A user selects:

``` text
Property Type: Land / Plot
Location: Gachibowli, Hyderabad
Area: 200 sq yd
Currency: INR
```

The system searches for current land/plot price evidence and provides an
estimated price based on the available web evidence.

### Useful for

-   Plot buyers
-   Land investors
-   Property researchers
-   Real-estate agents
-   Initial budget planning

------------------------------------------------------------------------

## 2. Flat / Apartment Price Research

A user selects:

``` text
Property Type: Flat / Apartment
BHK: 2 BHK
Location: Gachibowli, Hyderabad
Area: 1200 sq ft
Status: Ready to Move
```

The system searches specifically for the selected BHK and location.

### Useful questions

-   What is the estimated price of a 1 BHK?
-   What is the average price of a 2 BHK?
-   How much does a 3 BHK cost in a particular locality?
-   What is the approximate price per square foot?

------------------------------------------------------------------------

## 3. Villa Price Research

Example:

``` text
Property Type: Villa
BHK: 3 BHK
Location: Hyderabad
Area: 2500 sq ft
```

The application searches for 3 BHK villa pricing and extracts available
price and market information.

------------------------------------------------------------------------

## 4. Independent House Price Research

Example:

``` text
Property Type: Independent House
BHK: 3 BHK
Location: Kukatpally, Hyderabad
Area: 1800 sq ft
```

The system searches for 3 BHK independent houses in the selected
location.

------------------------------------------------------------------------

## 5. Commercial Property Price Research

Commercial property does **not** use BHK.

The user selects a commercial category such as:

-   Shop
-   Office
-   Showroom
-   Warehouse
-   Commercial Building

Example:

``` text
Property Type: Commercial Property
Commercial Type: Shop
Location: Gachibowli, Hyderabad
Area: 1000 sq ft
```

The search is then focused on commercial shop pricing rather than
residential BHK pricing.

------------------------------------------------------------------------

# 🏘️ Supported Property Types

  Property Type              BHK   Area / Unit in Price Mode   Commercial Type
  ------------------------ ----- --------------------------- -----------------
  🌳 Land / Plot              ❌                          ✅                ❌
  🏢 Flat / Apartment         ✅                          ✅                ❌
  🏡 Villa                    ✅                          ✅                ❌
  🏠 Independent House        ✅                          ✅                ❌
  🏬 Commercial Property      ❌                          ✅                ✅

------------------------------------------------------------------------

# 🏢 BHK Rules

BHK is relevant to residential properties.

### Flat / Apartment

``` text
1 BHK
2 BHK
3 BHK
4 BHK
5+ BHK
```

### Villa

``` text
1 BHK
2 BHK
3 BHK
4 BHK
5+ BHK
```

### Independent House

``` text
1 BHK
2 BHK
3 BHK
4 BHK
5+ BHK
```

### Land / Plot

BHK is hidden.

### Commercial Property

BHK is hidden.

This logic is enforced in both the frontend and backend validation.

------------------------------------------------------------------------

# 🏬 Commercial Property Rules

Commercial properties use a **Commercial Type** instead of BHK.

Available types:

``` text
Shop
Office
Showroom
Warehouse
Commercial Building
```

Example search:

``` text
Shop price in Gachibowli Hyderabad
```

instead of:

``` text
2 BHK shop in Gachibowli
```

This prevents residential BHK concepts from being incorrectly applied to
commercial properties.

------------------------------------------------------------------------

# 💰 Price Analysis

The **Price** mode is intended to answer:

> "How much does this property approximately cost?"

The frontend dynamically displays the relevant inputs.

Typical price-mode inputs:

``` text
Location
Property Type
BHK / Commercial Type
Property Status
Area
Area Unit
Currency
```

For residential properties:

``` text
Flat + 2 BHK
Villa + 3 BHK
Independent House + 3 BHK
```

For commercial:

``` text
Commercial + Shop
Commercial + Office
```

For land:

``` text
Land / Plot
```

------------------------------------------------------------------------

# 💸 Affordability Analysis

The **Affordability** mode is intended to answer:

> "Given my budget and location, what property options and areas should
> I investigate?"

For residential property affordability, the user provides:

``` text
Location
Budget
Currency
Property Type
BHK
```

### No area or area unit is required in property affordability mode.

For example:

``` text
Property Type: Flat / Apartment
BHK: 2 BHK
Location: Hyderabad
Budget: ₹80,00,000
Currency: INR
```

The application then searches for locality-level price evidence.

------------------------------------------------------------------------

# 🗺️ City and Locality Analysis

One of the major affordability features is **city-to-locality
analysis**.

Instead of returning only:

``` text
Hyderabad average: ₹X
```

the application attempts to identify recognizable areas within the
requested city and provide locality-level evidence.

Conceptually:

``` text
Hyderabad
│
├── Locality A → Estimated price
├── Locality B → Estimated price
├── Locality C → Estimated price
├── Locality D → Estimated price
└── Locality E → Estimated price
```

The results can include:

-   Area / locality
-   Average property price
-   Minimum price when available
-   Maximum price when available
-   Price per square foot
-   Estimated affordable area when price/sq-ft evidence exists
-   Source information

The backend performs multiple complementary Tavily searches rather than
depending on a single city-wide query.

Examples of search intent include:

``` text
2 BHK flat price by locality in Hyderabad
2 BHK flat for sale Hyderabad localities
property rates in Hyderabad areas 2 BHK
```

For commercial property:

``` text
shop price by locality in Hyderabad
commercial property rates in Hyderabad areas
```

For land:

``` text
land plot price by locality in Hyderabad
land rates in Hyderabad main areas
```

------------------------------------------------------------------------

# 🤖 How the AI Pipeline Works

## Step 1 --- User Input

The user selects:

``` text
Property Type
Location
BHK / Commercial Type
Area / Unit (Price mode)
Budget (Affordability mode)
Currency
Property Status where applicable
```

------------------------------------------------------------------------

## Step 2 --- Location Search

The frontend uses OpenStreetMap Nominatim to:

-   Search cities
-   Search localities
-   Search addresses
-   Search landmarks
-   Provide location suggestions

The browser's Geolocation API can also be used through:

``` text
Use my current location
```

The selected coordinates can be used for the result map.

------------------------------------------------------------------------

## Step 3 --- Query Generation

The backend generates a property-specific search query.

Examples:

``` text
2 BHK flat price in Gachibowli Hyderabad
```

``` text
3 BHK villa price in Hyderabad
```

``` text
3 BHK independent house price in Hyderabad
```

``` text
commercial shop price in Hyderabad
```

``` text
land plot price in Hyderabad
```

------------------------------------------------------------------------

## Step 4 --- Tavily Web Search

Tavily retrieves current web evidence.

The backend collects:

-   Search answer
-   Result titles
-   URLs
-   Result excerpts

Multiple searches are merged for locality affordability analysis.

Duplicate results are removed using URL/result information.

------------------------------------------------------------------------

## Step 5 --- Gemini Extraction

The retrieved evidence is passed to Gemini.

Gemini is instructed to extract structured information such as:

``` json
{
  "price_per_unit": 7850,
  "unit": "sq ft",
  "currency": "INR",
  "average_price": 9200000,
  "min_price": 7800000,
  "max_price": 11500000,
  "average_price_per_sqft": 7850,
  "typical_area_min": 1050,
  "typical_area_max": 1350,
  "sample_size": 18,
  "market_trend": "moderate demand",
  "confidence": "medium"
}
```

The model is instructed not to invent unsupported prices.

------------------------------------------------------------------------

## Step 6 --- Backend Validation

The FastAPI backend validates the extracted response.

For example:

-   Residential property without BHK → `422`
-   Commercial property with BHK → `422`
-   Commercial property without Commercial Type → `422`
-   Unsupported property type → `422`
-   Search failure → `502`
-   Gemini extraction failure → `502`
-   No usable price evidence → `404` in price analysis
-   Insufficient locality-level evidence → validation/error response in
    affordability analysis

------------------------------------------------------------------------

## Step 7 --- Result Dashboard

The frontend displays:

-   Estimated price
-   Typical price range
-   Price per sq ft
-   Typical area
-   Market trend
-   Confidence
-   Location map when coordinates are available
-   AI market summary
-   Web sources

Affordability results additionally display locality-level comparisons.

------------------------------------------------------------------------

# 🏗️ System Architecture

``` text
                    ┌───────────────────────┐
                    │       User            │
                    │  Web Browser / PC     │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ React + TypeScript    │
                    │ Vite Frontend         │
                    └───────────┬───────────┘
                                │ HTTP
                                ▼
                    ┌───────────────────────┐
                    │ FastAPI Backend       │
                    │ Property Validation   │
                    │ Query Orchestration   │
                    └───────┬────────┬──────┘
                            │        │
                 ┌──────────┘        └──────────┐
                 ▼                               ▼
        ┌─────────────────┐            ┌─────────────────┐
        │ Tavily Search   │            │ Gemini AI       │
        │ Current Web     │───────────▶│ Extraction      │
        │ Evidence        │            │ Structured JSON │
        └─────────────────┘            └────────┬────────┘
                                                │
                                                ▼
                                      ┌──────────────────┐
                                      │ FastAPI Response │
                                      └────────┬─────────┘
                                               │
                                               ▼
                                      ┌──────────────────┐
                                      │ Results Dashboard│
                                      └──────────────────┘
```

------------------------------------------------------------------------

# 🛠️ Technology Stack

## Frontend

-   React
-   TypeScript
-   Vite
-   Lucide React
-   CSS
-   Browser Geolocation API
-   OpenStreetMap / Nominatim
-   OpenStreetMap map embed

## Backend

-   Python
-   FastAPI
-   Pydantic
-   Uvicorn
-   HTTPX
-   python-dotenv

## AI / Search

-   Google Gemini
-   Tavily Search

## Location

-   OpenStreetMap Nominatim

## Development

-   Node.js
-   npm
-   Python virtual environment / Conda environment
-   Git / GitHub

------------------------------------------------------------------------

# 📁 Project Structure

``` text
LandWise_AI_Property/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── unit_utils.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── tavily_service.py
│   │       └── gemini_service.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── styles.css
│   │   └── vite-env.d.ts
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
│
├── README.md
└── package-lock.json
```

------------------------------------------------------------------------

# 🎨 Frontend

The frontend provides a compact property-analysis dashboard.

## Main sections

### Property selector

``` text
🌳 Land / Plot
🏢 Flat / Apartment
🏡 Villa
🏠 Independent House
🏬 Commercial Property
```

### Analysis modes

``` text
Price
Affordability
```

### Dynamic fields

The interface changes depending on the selected property type.

For example:

``` text
Flat
→ BHK appears

Villa
→ BHK appears

Independent House
→ BHK appears

Commercial
→ Commercial Type appears

Land
→ BHK does not appear
```

------------------------------------------------------------------------

# ⚙️ Backend

The FastAPI backend is responsible for:

1.  Receiving frontend requests
2.  Validating property requirements
3.  Building Tavily queries
4.  Calling Tavily
5.  Sending evidence to Gemini
6.  Extracting structured property information
7.  Validating extracted prices
8.  Returning JSON responses
9.  Providing source URLs

------------------------------------------------------------------------

# 🔌 API Endpoints

## `GET /`

Backend status endpoint.

Example response:

``` json
{
  "status": "ok",
  "message": "LandWise AI Property API is running.",
  "docs": "/docs"
}
```

------------------------------------------------------------------------

## `GET /health`

Health-check endpoint.

``` json
{
  "status": "healthy",
  "service": "LandWise AI Property",
  "version": "4.0.0"
}
```

------------------------------------------------------------------------

## `POST /property-price`

Main price-analysis endpoint.

Used by the frontend **Price** mode.

------------------------------------------------------------------------

## `GET /land-price`

Legacy/specialized land-price endpoint.

It is retained for compatibility with the original land-price
functionality.

------------------------------------------------------------------------

## `POST /affordability`

Affordability endpoint.

Used to determine locality-level property information based on:

-   Location
-   Budget
-   Property type
-   BHK for residential properties
-   Commercial type for commercial properties

------------------------------------------------------------------------

# 📦 Request Examples

## Flat / Apartment Price

``` json
{
  "property_type": "flat",
  "location": "Gachibowli, Hyderabad",
  "bhk": "2 BHK",
  "area": 1200,
  "area_unit": "sq ft",
  "property_status": "Ready to Move",
  "currency": "INR"
}
```

------------------------------------------------------------------------

## Villa Price

``` json
{
  "property_type": "villa",
  "location": "Hyderabad",
  "bhk": "3 BHK",
  "area": 2500,
  "area_unit": "sq ft",
  "property_status": "Ready to Move",
  "currency": "INR"
}
```

------------------------------------------------------------------------

## Independent House Price

``` json
{
  "property_type": "independent_house",
  "location": "Kukatpally, Hyderabad",
  "bhk": "3 BHK",
  "area": 1800,
  "area_unit": "sq ft",
  "property_status": "Resale",
  "currency": "INR"
}
```

------------------------------------------------------------------------

## Commercial Property Price

``` json
{
  "property_type": "commercial",
  "location": "Gachibowli, Hyderabad",
  "commercial_type": "shop",
  "area": 1000,
  "area_unit": "sq ft",
  "currency": "INR"
}
```

Notice that there is **no BHK**.

------------------------------------------------------------------------

## Land Price

``` json
{
  "property_type": "land",
  "location": "Gachibowli, Hyderabad",
  "area": 200,
  "area_unit": "sq yd",
  "currency": "INR"
}
```

------------------------------------------------------------------------

## Residential Affordability

``` json
{
  "location": "Hyderabad",
  "budget": 8000000,
  "currency": "INR",
  "property_type": "flat",
  "bhk": "2 BHK"
}
```

Area and area unit are intentionally not required for property
affordability.

------------------------------------------------------------------------

## Commercial Affordability

``` json
{
  "location": "Hyderabad",
  "budget": 10000000,
  "currency": "INR",
  "property_type": "commercial",
  "commercial_type": "shop"
}
```

No BHK and no area/unit are required for commercial affordability.

------------------------------------------------------------------------

# 🔐 Environment Variables

Create:

``` text
backend/.env
```

Example:

``` env
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODELS=gemini-2.5-flash-lite,gemini-2.5-flash
```

Optional frontend configuration:

``` text
frontend/.env
```

``` env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

For same-origin production serving, the frontend can use an empty API
base:

``` env
VITE_API_BASE_URL=
```

------------------------------------------------------------------------

# 📥 Installation

## Prerequisites

Install:

-   Python 3.10+
-   Node.js 18+
-   npm
-   Tavily API key
-   Gemini API key

------------------------------------------------------------------------

## 1. Clone the repository

``` bash
git clone <your-github-repository-url>
cd LandWise_AI_Property
```

------------------------------------------------------------------------

## 2. Create a Python environment

Using Conda:

``` bash
conda create -n landwise python=3.13
conda activate landwise
```

Or using Python virtual environment:

``` bash
python -m venv .venv
```

Windows:

``` cmd
.venv\Scripts\activate
```

------------------------------------------------------------------------

## 3. Install backend dependencies

``` bash
cd backend
python -m pip install -r requirements.txt
```

------------------------------------------------------------------------

## 4. Configure API keys

Create:

``` text
backend/.env
```

Add:

``` env
TAVILY_API_KEY=your_key
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODELS=gemini-2.5-flash-lite,gemini-2.5-flash
```

Never commit `.env` to GitHub.

------------------------------------------------------------------------

# ▶️ Running the Application

## Start Backend

From the project root:

``` cmd
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend:

``` text
http://127.0.0.1:8000
```

Swagger documentation:

``` text
http://127.0.0.1:8000/docs
```

Health check:

``` text
http://127.0.0.1:8000/health
```

------------------------------------------------------------------------

## Start Frontend

Open another terminal:

``` cmd
cd frontend
npm install
npm run dev
```

Vite normally provides a local URL such as:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

# 🏭 Production Frontend Build

Build the React application:

``` cmd
cd frontend
npm run build
```

The generated production files will be placed in:

``` text
frontend/dist/
```

The FastAPI application is designed to serve the production frontend
when the built files are available in the expected location.

------------------------------------------------------------------------

# 📍 Location Search

LandWise AI supports location discovery using OpenStreetMap Nominatim.

Users can search:

``` text
City
Locality
Address
Landmark
```

Example:

``` text
Gachibowli
Hyderabad
Bengaluru
Madhapur
Kondapur
```

The interface displays matching location suggestions.

Users can also use:

``` text
Use my current location
```

when browser location permission is available.

------------------------------------------------------------------------

# 🔄 Gemini Reliability and Retry Handling

Gemini can temporarily return errors such as:

``` text
503 UNAVAILABLE
429 RESOURCE EXHAUSTED
500 INTERNAL SERVER ERROR
502 BAD GATEWAY
504 GATEWAY TIMEOUT
```

LandWise AI includes retry handling for temporary Gemini failures.

The service:

1.  Calls the configured Gemini model.
2.  Retries temporary server/rate-limit errors.
3.  Uses exponential backoff.
4.  Attempts configured fallback models.
5.  Returns a controlled backend error if extraction still cannot be
    completed.

Example configuration:

``` env
GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODELS=gemini-2.5-flash-lite,gemini-2.5-flash
```

This reduces failures caused by temporary model availability issues.

------------------------------------------------------------------------

# ❗ Error Handling

The application intentionally distinguishes different failure cases.

## `422`

Validation problem.

Examples:

``` text
BHK is required for residential property.
```

``` text
BHK is not applicable to Commercial Property.
```

``` text
Commercial Type is required.
```

------------------------------------------------------------------------

## `502`

External service problem.

Examples:

``` text
Tavily search failed.
```

``` text
Gemini extraction failed.
```

------------------------------------------------------------------------

## `404`

Price analysis may return `404` when the web evidence does not contain a
usable property price.

Example:

``` text
No usable property-price evidence was extracted.
```

This is different from a missing API endpoint.

------------------------------------------------------------------------

## Affordability

Affordability depends on locality-level web evidence.

If a requested city does not provide enough structured locality
evidence, the application should explain that the available web evidence
is insufficient instead of presenting fabricated locality prices.

------------------------------------------------------------------------

# 📊 Data and Pricing Methodology

LandWise AI does **not** treat one web result as ground truth.

The process is:

``` text
Search multiple sources
        ↓
Collect relevant excerpts
        ↓
Send evidence to Gemini
        ↓
Extract supported numeric values
        ↓
Validate result
        ↓
Display estimate + sources
```

Potential information extracted includes:

-   Average property price
-   Minimum price
-   Maximum price
-   Price per square foot
-   Typical property area
-   Number of comparable results
-   Market trend text
-   Confidence level
-   Source URLs

------------------------------------------------------------------------

# ⚠️ Important Pricing Disclaimer

Property prices can vary significantly because of:

-   Exact locality
-   Street
-   Building age
-   Floor
-   Facing
-   Parking
-   Amenities
-   Gated-community status
-   Construction quality
-   Plot dimensions
-   Road width
-   Commercial usage
-   Property condition
-   Negotiation
-   Seller expectations
-   Market conditions

Online property portals commonly show **asking prices**, which may
differ from final transaction prices.

Therefore:

> LandWise AI should be treated as a property research and estimation
> tool, not as an official valuation or guaranteed sale-price system.

------------------------------------------------------------------------

# 🔒 Security

## API Keys

Do not put Tavily or Gemini API keys in:

-   React source code
-   TypeScript files
-   GitHub repositories
-   Public frontend `.env` variables

The keys should remain on the backend.

Correct:

``` text
React
  ↓
FastAPI
  ↓
Tavily / Gemini
```

Avoid:

``` text
React
  ↓
Tavily API key
```

------------------------------------------------------------------------

## `.gitignore`

A recommended `.gitignore`:

``` gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Environment
.env
*.env

# Node
node_modules/
frontend/dist/

# Build
build/
dist/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

------------------------------------------------------------------------

# ⚠️ Limitations

LandWise AI currently depends on external web and AI services.

Possible limitations include:

### 1. Search coverage

Some localities may not have enough publicly available property-price
information.

### 2. Asking vs transaction price

Web listings can represent seller asking prices.

### 3. AI extraction

Gemini extracts information from retrieved evidence, so the quality of
the output depends partly on the quality and clarity of the evidence.

### 4. API availability

Tavily and Gemini can experience:

-   Rate limits
-   Temporary outages
-   Network failures
-   Model availability issues

### 5. Locality identification

City-level affordability attempts to identify major localities from
available evidence. It does not guarantee that every locality in a city
is represented.

### 6. Currency

Currency formatting and conversion should not be interpreted as a live
financial exchange-rate service unless a dedicated FX source is added.

------------------------------------------------------------------------

# 🚀 Future Enhancements

Potential next versions can add:

## Property Comparison

Compare:

``` text
2 BHK vs 3 BHK
Flat vs Villa
Locality A vs Locality B
```

------------------------------------------------------------------------

## Historical Price Trends

Store previous searches and visualize:

``` text
2024
2025
2026
```

with historical price movement.

------------------------------------------------------------------------

## Price Forecasting

Add an ML/AI forecasting layer using historical property data.

------------------------------------------------------------------------

## Property Recommendations

Example:

``` text
Budget: ₹80 lakh
City: Hyderabad
2 BHK
```

Return areas that have evidence of properties around the requested
budget.

------------------------------------------------------------------------

## Saved Properties

Allow users to save:

-   Location
-   Property type
-   BHK
-   Budget
-   Search history

------------------------------------------------------------------------

## Price Alerts

Notify users when:

``` text
2 BHK prices fall below ₹80 lakh
```

or:

``` text
A saved locality changes significantly.
```

------------------------------------------------------------------------

## Map-Based Property Intelligence

Potential integration with:

-   Google Maps
-   GIS data
-   Nearby roads
-   Metro stations
-   Schools
-   Hospitals
-   Shopping areas
-   Airports
-   Infrastructure projects

------------------------------------------------------------------------

## Satellite / GIS Analysis

Future versions could analyze:

-   Land surroundings
-   Development patterns
-   Road access
-   Nearby construction
-   Urban expansion

------------------------------------------------------------------------

## Property Investment Assistant

An AI assistant could answer:

``` text
Which areas are within my budget?
What is the approximate price range?
What factors may affect the price?
What nearby infrastructure should I investigate?
```

The assistant should present evidence and uncertainty rather than
treating its output as guaranteed investment advice.

------------------------------------------------------------------------

# 🧪 Development Workflow

Recommended workflow:

``` text
1. Start FastAPI
       ↓
2. Start React/Vite
       ↓
3. Test /health
       ↓
4. Test /docs
       ↓
5. Test Price mode
       ↓
6. Test Affordability mode
       ↓
7. Test every property type
       ↓
8. Test BHK validation
       ↓
9. Test Commercial validation
       ↓
10. Test Gemini/Tavily failures
       ↓
11. Build frontend
       ↓
12. Test production serving
```

------------------------------------------------------------------------

# ✅ Property-Type Test Matrix

Before releasing a new version, test:

  Property              Price   Affordability   BHK              Area
  ------------------- ------- --------------- ----- -----------------
  Land / Plot              ✅              ✅    ❌   Price mode only
  Flat / Apartment         ✅              ✅    ✅   Price mode only
  Villa                    ✅              ✅    ✅   Price mode only
  Independent House        ✅              ✅    ✅   Price mode only
  Commercial               ✅              ✅    ❌   Price mode only

Commercial affordability must use:

``` text
Commercial Type
```

rather than BHK.

Residential affordability must use:

``` text
BHK
```

but does not require area/unit.

------------------------------------------------------------------------

# 🐛 Troubleshooting

## Backend returned 404

First check:

``` text
http://127.0.0.1:8000/
```

Then:

``` text
http://127.0.0.1:8000/docs
```

If `/docs` does not contain:

``` text
POST /property-price
POST /affordability
```

you may be running an older backend.

Stop the existing process:

``` cmd
Ctrl+C
```

Then restart:

``` cmd
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

------------------------------------------------------------------------

## Gemini 503

A message such as:

``` text
Gemini returned 503 UNAVAILABLE
```

normally indicates temporary model/service unavailability.

Check:

``` env
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODELS=gemini-2.5-flash-lite,gemini-2.5-flash
```

Restart the backend after changing `.env`.

------------------------------------------------------------------------

## Tavily search failure

Check:

``` env
TAVILY_API_KEY=...
```

Then restart FastAPI.

------------------------------------------------------------------------

## Frontend cannot reach backend

Check that FastAPI is running:

``` text
http://127.0.0.1:8000/health
```

If using Vite separately, configure:

``` env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Then restart Vite.

------------------------------------------------------------------------

## React build error involving `import.meta.env`

Make sure this file exists:

``` text
frontend/src/vite-env.d.ts
```

with:

``` typescript
/// <reference types="vite/client" />
```

Then run:

``` cmd
npm run build
```

------------------------------------------------------------------------

# 📦 Production / Deployment

For a production deployment, the application can be hosted as:

``` text
                  Internet
                     │
                     ▼
              Reverse Proxy
                     │
              ┌──────┴──────┐
              ▼             ▼
          React UI       FastAPI
                            │
                     ┌──────┴──────┐
                     ▼             ▼
                   Tavily        Gemini
```

For local demonstrations, FastAPI can serve the built React application
directly.

For public deployment, additional security controls should be
considered:

-   HTTPS
-   Authentication
-   Rate limiting
-   Request validation
-   API key protection
-   Logging
-   Monitoring
-   CORS restrictions
-   Abuse protection

------------------------------------------------------------------------

# 🤝 Contributing

Contributions are welcome.

Suggested process:

``` bash
git checkout -b feature/property-comparison
```

Make changes, test the application, then:

``` bash
git add .
git commit -m "Add property comparison feature"
git push origin feature/property-comparison
```

Open a Pull Request on GitHub.

------------------------------------------------------------------------

# 📌 Project Status

**LandWise AI --- Property Intelligence**

Current capabilities:

-   ✅ Land / Plot price analysis
-   ✅ Flat / Apartment price analysis
-   ✅ 1--5+ BHK selection
-   ✅ Villa price analysis
-   ✅ Independent House price analysis
-   ✅ Commercial property analysis
-   ✅ Shop / Office / Showroom / Warehouse / Commercial Building
-   ✅ Location search
-   ✅ Browser current-location support
-   ✅ Area and unit selection in Price mode
-   ✅ Property affordability without area/unit
-   ✅ City/locality affordability research
-   ✅ Tavily web evidence
-   ✅ Gemini structured extraction
-   ✅ Gemini retry/fallback handling
-   ✅ Source links
-   ✅ Price ranges
-   ✅ Price per square foot
-   ✅ Market snapshot
-   ✅ Result map when coordinates are available
-   ✅ FastAPI Swagger documentation
-   ✅ React + TypeScript dashboard

------------------------------------------------------------------------

# 👨‍💻 Author

**LandWise AI**

AI-powered real-estate property price intelligence built with:

``` text
Python
FastAPI
React
TypeScript
Tavily
Google Gemini
OpenStreetMap
```

------------------------------------------------------------------------

# ⭐ Support

If you find the project useful, consider giving the repository a ⭐ on
GitHub.

For bugs or feature requests, create a GitHub Issue with:

``` text
Problem description
Property type
Location
Expected behavior
Actual behavior
Backend error
Frontend error
Screenshots if applicable
```

------------------------------------------------------------------------

## 📜 License

Add your preferred open-source license here, for example:

``` text
MIT License
```

or use a proprietary/company license if this project is not intended for
open-source distribution.
