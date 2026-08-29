"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - MAIN BACKEND API SERVER (FASTAPI)
==============================================================================
Description:
    Core API service connecting the AI Vision/NLP engine, Fair Pricing engine,
    and ONDC schema exporter. Serves the web frontend at http://localhost:8000.
==============================================================================
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

# Import our modular backend engines
from backend.pricing_engine import calculate_fair_price
from backend.ai_engine import analyze_craft_input
from backend.ondc_schema import export_to_beckn_ondc_catalog

app = FastAPI(
    title="AI Artisan Commerce Network API",
    description="Backend services for Voice-First Artisan Enablement & Fair Commerce",
    version="1.0.0"
)

# ----------------- Request Data Models -----------------
class CraftAnalyzeRequest(BaseModel):
    voice_transcript: str
    artisan_name: Optional[str] = "Savita Tai"
    artisan_region: Optional[str] = "Maharashtra"

class PriceCalculateRequest(BaseModel):
    material_cost: float
    labor_hours: float
    state_name: Optional[str] = "Maharashtra"
    desired_margin_pct: Optional[float] = 20.0
    packaging_cost: Optional[float] = 100.0
    artisan_intended_price: Optional[float] = None

class ONDCExportRequest(BaseModel):
    craft_data: dict
    artisan_name: Optional[str] = "Savita Tai"
    artisan_region: Optional[str] = "Maharashtra"


# ----------------- API Endpoints -----------------

@app.post("/api/analyze-craft", summary="Process Voice & Craft Input")
def api_analyze_craft(req: CraftAnalyzeRequest):
    """
    Analyzes spoken dialect, identifies craft category, and generates
    the heritage story and marketing kit.
    """
    result = analyze_craft_input(
        raw_voice_text=req.voice_transcript,
        artisan_name=req.artisan_name,
        artisan_region=req.artisan_region
    )
    return {"status": "success", "data": result}


@app.post("/api/calculate-price", summary="Compute Fair Pricing & Wage Math")
def api_calculate_price(req: PriceCalculateRequest):
    """
    Calculates cost-plus fair price based on state wage standards and alerts underpricing.
    """
    result = calculate_fair_price(
        material_cost=req.material_cost,
        labor_hours=req.labor_hours,
        state_name=req.state_name,
        desired_margin_pct=req.desired_margin_pct,
        packaging_cost=req.packaging_cost,
        artisan_intended_price=req.artisan_intended_price
    )
    return {"status": "success", "data": result}


@app.post("/api/export-ondc", summary="Generate ONDC Beckn Protocol JSON-LD")
def api_export_ondc(req: ONDCExportRequest):
    """
    Generates standard Beckn Protocol schema for ONDC network discovery.
    """
    result = export_to_beckn_ondc_catalog(
        product_data=req.craft_data,
        artisan_name=req.artisan_name,
        region=req.artisan_region
    )
    return {"status": "success", "data": result}


# ----------------- Serve Frontend Web App -----------------
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_home():
        return FileResponse(os.path.join(frontend_path, "index.html"))

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 AI Artisan Commerce Network Server starting at http://localhost:8000\n")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)