"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - MAIN BACKEND API SERVER (FASTAPI)
==============================================================================
"""

import os
import sys
import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Database and Seed
from backend.db import get_connection, init_db
from backend.seed_data import seed_database

# Domain Services & Engines
from backend.models import (
    AuthLoginRequest, ArtisanOnboardingRequest, CraftAnalyzeRequest,
    ImageAnalysisRequest, PriceCalculateRequest, GIVerifyRequest,
    ProductCreateRequest, OrderCreateRequest, OrderStateUpdateRequest,
    ChatMessageRequest, ReviewCreateRequest, AIAssistantQueryRequest,
    PincodeCheckRequest, EscrowState
)
from backend.auth_service import authenticate_user, onboard_artisan, get_all_demo_personas
from backend.pricing_engine import calculate_fair_price, get_statutory_wage
from backend.ai_engine import (
    analyze_craft_input, analyze_craft_image,
    answer_ai_assistant_query, generate_marketing_kit
)
from backend.gi_service import verify_gi_certificate, list_all_gi_records
from backend.payment_escrow import get_payment_gateway, transition_order_state, STATE_METADATA
from backend.logistics_service import check_pincode_serviceability, get_order_tracking_timeline
from backend.chat_service import post_chat_message, get_order_messages
from backend.fraud_demand_engine import check_product_authenticity_and_fraud, get_craft_demand_forecasts
from backend.admin_service import get_admin_dashboard_metrics, admin_review_artisan, get_admin_audit_logs
from backend.ondc_schema import export_to_beckn_ondc_catalog, generate_beckn_flow_step

app = FastAPI(
    title="AI Artisan Commerce Network API",
    description="Autonomous Fair-Wage AI Digital Layer for Indian Artisans (SIH 2026)",
    version="2.0.0"
)

# CORS for local and web dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure DB and Seeds are initialized
init_db()
seed_database()


# ----------------- 1. AUTHENTICATION & ONBOARDING -----------------

@app.post("/api/auth/login", summary="Login via Mobile/Email/Vishwakarma/Demo")
def api_auth_login(req: AuthLoginRequest):
    return authenticate_user(req)


@app.get("/api/auth/demo-personas", summary="List All Demo Personas (Artisans, Buyers, Admin)")
def api_demo_personas():
    return {"status": "success", "data": get_all_demo_personas()}


@app.post("/api/admin/reseed", summary="Reseed Database with Full Multi-Persona Dataset")
def api_admin_reseed():
    seed_database(force=True)
    return {"status": "success", "message": "Database reseeded successfully with 8 Artisans, 6 Buyers, and linked Orders."}


@app.post("/api/upload-image", summary="Upload/Drop Product Image with AI Vision Analysis")
def api_upload_image(payload: Dict[str, Any]):
    image_data = payload.get("image_data") or payload.get("image_url") or "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600"
    craft_hint = payload.get("craft_hint", "")
    analysis = analyze_craft_image(image_data, craft_hint)
    return {
        "status": "success",
        "image_url": image_data,
        "ai_analysis": analysis
    }


@app.post("/api/artisan/onboard", summary="Submit Artisan Onboarding Application")
def api_artisan_onboard(req: ArtisanOnboardingRequest):
    res = onboard_artisan(req)
    return {"status": "success", "data": res}


# ----------------- 2. AI DIGITIZATION, VOICE & VISION -----------------

@app.post("/api/analyze-craft", summary="Voice-to-Catalog NLP & Extraction")
def api_analyze_craft(req: CraftAnalyzeRequest):
    res = analyze_craft_input(
        raw_voice_text=req.voice_transcript,
        artisan_name=req.artisan_name or "Savita Tai",
        artisan_region=req.artisan_region or "Maharashtra",
        language=req.language or "mr-IN"
    )
    return {"status": "success", "data": res}


@app.post("/api/analyze-image", summary="AI Vision Inspection & Motif Detection")
def api_analyze_image(req: ImageAnalysisRequest):
    res = analyze_craft_image(image_url=req.image_url, craft_hint=req.craft_hint)
    return {"status": "success", "data": res}


@app.post("/api/assistant/query", summary="Contextual AI Assistant for Artisan & Buyer")
def api_assistant_query(req: AIAssistantQueryRequest):
    res = answer_ai_assistant_query(user_role=req.user_role, query=req.query, context=req.context_data)
    return {"status": "success", "data": res}


# ----------------- 3. STATUTORY WAGE & FAIR PRICING -----------------

@app.post("/api/calculate-price", summary="Compute Fair Wage Math & Underpricing Defense")
def api_calculate_price(req: PriceCalculateRequest):
    res = calculate_fair_price(
        material_cost=req.material_cost,
        labor_hours=req.labor_hours,
        state_name=req.state_name or "Maharashtra",
        craft_name=req.craft_name,
        skill_level=req.skill_level or "Skilled",
        desired_margin_pct=req.desired_margin_pct or 20.0,
        packaging_cost=req.packaging_cost or 100.0,
        logistics_cost=req.logistics_cost or 150.0,
        overhead_cost=req.overhead_cost or 100.0,
        artisan_intended_price=req.artisan_intended_price
    )
    return {"status": "success", "data": res}


@app.get("/api/wage-benchmarks", summary="Get State Statutory Artisan Wage Benchmarks")
def api_wage_benchmarks(state: Optional[str] = "Maharashtra"):
    res = get_statutory_wage(state_name=state)
    return {"status": "success", "data": res}


# ----------------- 4. GI VERIFICATION -----------------

@app.post("/api/gi/verify", summary="Verify GI Certificate against National Registry")
def api_gi_verify(req: GIVerifyRequest):
    res = verify_gi_certificate(req)
    return {"status": "success", "data": res}


@app.get("/api/gi/records", summary="List Official Registered GI Crafts")
def api_gi_records():
    res = list_all_gi_records()
    return {"status": "success", "data": res}


# ----------------- 5. PRODUCTS & MARKETPLACE -----------------

@app.get("/api/products", summary="Browse Marketplace Products with Filters")
def api_get_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    state: Optional[str] = None,
    gi_only: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    artisan_id: Optional[int] = None
):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if search:
        s_clean = f"%{search.strip().lower()}%"
        query += " AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ? OR LOWER(craft_type) LIKE ? OR LOWER(state_cluster) LIKE ?)"
        params.extend([s_clean, s_clean, s_clean, s_clean])
        
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
        
    if state and state != "All":
        query += " AND state_cluster = ?"
        params.append(state)
        
    if gi_only:
        query += " AND gi_verified = 1"
        
    if min_price is not None:
        query += " AND selling_price >= ?"
        params.append(min_price)
        
    if max_price is not None:
        query += " AND selling_price <= ?"
        params.append(max_price)
        
    if artisan_id is not None:
        query += " AND artisan_id = ?"
        params.append(artisan_id)
        
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    products = []
    for r in rows:
        p = dict(r)
        p["materials"] = json.loads(p["materials"]) if p["materials"] else []
        p["motifs"] = json.loads(p["motifs"]) if p["motifs"] else []
        p["image_urls"] = json.loads(p["image_urls"]) if p["image_urls"] else []
        p["tags"] = json.loads(p["tags"]) if p["tags"] else []
        products.append(p)
        
    conn.close()
    return {"status": "success", "count": len(products), "data": products}


@app.get("/api/products/{product_id}", summary="Get Product Details")
def api_get_product_detail(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET view_count = view_count + 1 WHERE id = ?", (product_id,))
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
        
    p = dict(row)
    p["materials"] = json.loads(p["materials"]) if p["materials"] else []
    p["motifs"] = json.loads(p["motifs"]) if p["motifs"] else []
    p["image_urls"] = json.loads(p["image_urls"]) if p["image_urls"] else []
    p["tags"] = json.loads(p["tags"]) if p["tags"] else []
    
    # Get Reviews
    cursor.execute("SELECT * FROM reviews WHERE product_id = ? ORDER BY id DESC", (product_id,))
    reviews = [dict(r) for r in cursor.fetchall()]
    p["reviews"] = reviews
    
    conn.commit()
    conn.close()
    return {"status": "success", "data": p}


@app.post("/api/products", summary="Create and Publish Artisan Product")
def api_create_product(req: ProductCreateRequest):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    cursor.execute("""
    INSERT INTO products (artisan_id, artisan_name, title, short_description, description, heritage_story,
        category, craft_type, state_cluster, materials, technique, motifs, dimensions, weight,
        care_instructions, image_urls, material_cost, labor_hours, hourly_wage_rate, suggested_fair_price,
        selling_price, stock_quantity, is_made_to_order, production_days, gi_number, gi_verified,
        tags, status, view_count, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        req.artisan_id or 1, req.artisan_name, req.title, req.short_description, req.description,
        req.heritage_story, req.category, req.craft_type, req.state_cluster, json.dumps(req.materials),
        req.technique, json.dumps(req.motifs), req.dimensions, req.weight, req.care_instructions,
        json.dumps(req.image_urls or ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&auto=format&fit=crop&q=80"]),
        req.material_cost, req.labor_hours, req.hourly_wage_rate, req.suggested_fair_price, req.selling_price,
        req.stock_quantity, 1 if req.is_made_to_order else 0, req.production_days, req.gi_number,
        1 if req.gi_verified else 0, json.dumps(req.tags), req.status.value, 0, now, now
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"status": "success", "product_id": new_id, "message": "Product published to marketplace and ONDC catalog."}


# ----------------- 6. ARTISANS / MEET THE MAKERS -----------------

@app.get("/api/artisans", summary="List Artisan Profiles")
def api_get_artisans():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artisans ORDER BY verified_orders_count DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    for r in rows:
        r["languages"] = json.loads(r["languages"]) if r["languages"] else []
    conn.close()
    return {"status": "success", "data": rows}


@app.get("/api/artisans/{artisan_id}", summary="Get Artisan Profile & Catalog")
def api_get_artisan_detail(artisan_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artisans WHERE id = ?", (artisan_id,))
    artisan = cursor.fetchone()
    if not artisan:
        conn.close()
        raise HTTPException(status_code=404, detail="Artisan not found")
        
    art_dict = dict(artisan)
    art_dict["languages"] = json.loads(art_dict["languages"]) if art_dict["languages"] else []
    
    cursor.execute("SELECT * FROM products WHERE artisan_name = ? OR artisan_id = ?", (art_dict["name"], artisan_id))
    products = [dict(p) for p in cursor.fetchall()]
    for p in products:
        p["image_urls"] = json.loads(p["image_urls"]) if p["image_urls"] else []
        p["tags"] = json.loads(p["tags"]) if p["tags"] else []
    art_dict["products"] = products
    
    conn.close()
    return {"status": "success", "data": art_dict}


# ----------------- 7. ORDERS, ESCROW & TRACKING -----------------

@app.post("/api/orders", summary="Place Order with Escrow Lock")
def api_create_order(req: OrderCreateRequest):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (req.product_id,))
    prod = cursor.fetchone()
    if not prod:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
        
    p = dict(prod)
    qty = max(req.quantity, 1)
    unit_price = p["selling_price"]
    total_amount = round(unit_price * qty, 2)
    
    # Calculate payout breakdown
    labor_wage = round(p["labor_hours"] * p["hourly_wage_rate"] * qty, 2)
    material_payout = round(p["material_cost"] * qty, 2)
    artisan_payout = round(labor_wage + material_payout + (total_amount * 0.15), 2)
    logistics_fee = 150.0
    platform_fee = round(total_amount * 0.03, 2)
    
    order_number = f"ORD-{datetime.utcnow().strftime('%Y')}-{uuid.uuid4().hex[:6].upper()}"
    tracking_number = f"IP-IN-{int(datetime.utcnow().timestamp()*1000) % 1000000000:09d}"
    est_delivery = (datetime.utcnow() + timedelta(days=p["production_days"] + 3)).strftime("%d %b %Y")
    now = datetime.utcnow().isoformat()
    
    # Insert Order
    cursor.execute("""
    INSERT INTO orders (order_number, product_id, product_title, product_image, artisan_id, artisan_name,
        buyer_id, buyer_name, buyer_phone, delivery_address, delivery_pincode, delivery_city, delivery_state,
        quantity, unit_price, total_amount, artisan_wage_payout, raw_material_payout, logistics_fee, platform_fee,
        payment_method, payment_status, escrow_state, carrier, tracking_number, estimated_delivery, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_number, p["id"], p["title"],
        json.loads(p["image_urls"])[0] if p["image_urls"] else "",
        p["artisan_id"], p["artisan_name"], req.buyer_id or 1, req.buyer_name, req.buyer_phone,
        req.delivery_address, req.delivery_pincode, req.delivery_city, req.delivery_state,
        qty, unit_price, total_amount, artisan_payout, material_payout, logistics_fee, platform_fee,
        req.payment_method, "AUTHORIZED", "PAYMENT_SECURED", "India Post SpeedPost (ONDC Logistics)",
        tracking_number, est_delivery, now, now
    ))
    order_id = cursor.lastrowid
    
    # Create Escrow record
    cursor.execute("""
    INSERT INTO escrow_records (order_id, order_number, total_held, artisan_share, platform_share, status, held_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order_id, order_number, total_amount, artisan_payout, platform_fee, "HELD", now))
    
    # Create Initial Tracking Event
    cursor.execute("""
    INSERT INTO tracking_events (order_id, status_key, title, description, location, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (order_id, "PAYMENT_SECURED", "Payment Secured in Trust Escrow",
          f"₹{total_amount:,.2f} locked in RBI-compliant escrow vault. Artisan notified to accept.",
          req.delivery_city, now))
          
    # Notify Artisan
    cursor.execute("""
    INSERT INTO notifications (recipient_role, recipient_id, title, message, event_type, is_read, action_url, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("ARTISAN", p["artisan_id"], "New Fair-Wage Order Received! 🎉",
          f"Order #{order_number} for '{p['title']}'. ₹{artisan_payout:,.2f} secured in Escrow.",
          "order", 0, "/artisan/orders", now))
          
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "order_id": order_id,
        "order_number": order_number,
        "escrow_state": "PAYMENT_SECURED",
        "artisan_wage_secured": artisan_payout,
        "tracking_number": tracking_number,
        "estimated_delivery": est_delivery,
        "message": f"Payment authorized. ₹{total_amount:,.2f} held in Escrow."
    }


@app.get("/api/orders", summary="Fetch Orders with Role & Persona Filter")
def api_get_orders(
    role: Optional[str] = "all",
    user_id: Optional[int] = None,
    artisan_name: Optional[str] = None,
    buyer_name: Optional[str] = None
):
    conn = get_connection()
    cursor = conn.cursor()
    
    if role.lower() == "artisan":
        if artisan_name:
            cursor.execute("""
            SELECT * FROM orders 
            WHERE LOWER(artisan_name) LIKE ? OR artisan_id = ?
            ORDER BY id DESC
            """, (f"%{artisan_name.strip().lower()}%", user_id or 0))
        elif user_id:
            cursor.execute("SELECT * FROM orders WHERE artisan_id = ? ORDER BY id DESC", (user_id,))
        else:
            cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    elif role.lower() == "buyer":
        if buyer_name:
            cursor.execute("""
            SELECT * FROM orders 
            WHERE LOWER(buyer_name) LIKE ? OR buyer_id = ?
            ORDER BY id DESC
            """, (f"%{buyer_name.strip().lower()}%", user_id or 0))
        elif user_id:
            cursor.execute("SELECT * FROM orders WHERE buyer_id = ? ORDER BY id DESC", (user_id,))
        else:
            cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    else:
        cursor.execute("SELECT * FROM orders ORDER BY id DESC")
        
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"status": "success", "data": rows}


@app.get("/api/orders/{order_id}", summary="Get Order Details with Tracking & Escrow")
def api_get_order_detail(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
        
    ord_dict = dict(order)
    
    # Fetch Tracking
    cursor.execute("SELECT * FROM tracking_events WHERE order_id = ? ORDER BY id ASC", (order_id,))
    ord_dict["tracking_timeline"] = [dict(r) for r in cursor.fetchall()]
    
    # Fetch Escrow
    cursor.execute("SELECT * FROM escrow_records WHERE order_id = ?", (order_id,))
    escrow = cursor.fetchone()
    ord_dict["escrow"] = dict(escrow) if escrow else None
    
    conn.close()
    return {"status": "success", "data": ord_dict}


@app.post("/api/orders/transition", summary="Advance Order/Escrow State Machine")
def api_order_transition(req: OrderStateUpdateRequest):
    res = transition_order_state(req.order_id, req.new_state, req.note, req.actor or "artisan")
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Transition failed"))
    return {"status": "success", "data": res}


@app.get("/api/orders/{order_id}/tracking", summary="Get Live Order Tracking Timeline")
def api_order_tracking(order_id: int):
    events = get_order_tracking_timeline(order_id)
    return {"status": "success", "data": events}


# ----------------- 8. LOGISTICS & PINCODES -----------------

@app.post("/api/logistics/check-pincode", summary="Check Pincode Serviceability")
def api_check_pincode(req: PincodeCheckRequest):
    res = check_pincode_serviceability(req.pincode)
    return {"status": "success", "data": res}


# ----------------- 9. CHAT & TRANSLATION -----------------

@app.post("/api/chat/messages", summary="Post Order Message with Indic Translation")
def api_post_message(req: ChatMessageRequest):
    res = post_chat_message(req)
    return {"status": "success", "data": res}


@app.get("/api/chat/{order_id}", summary="Get Chat History for Order")
def api_get_chat(order_id: int):
    msgs = get_order_messages(order_id)
    return {"status": "success", "data": msgs}


# ----------------- 10. REVIEWS & RATINGS -----------------

@app.post("/api/reviews", summary="Submit Verified Buyer Review")
def api_create_review(req: ReviewCreateRequest):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    cursor.execute("""
    INSERT INTO reviews (product_id, order_id, buyer_name, is_verified_purchase, rating, review_title, comment, created_at)
    VALUES (?, ?, ?, 1, ?, ?, ?, ?)
    """, (req.product_id, req.order_id, req.buyer_name, req.rating, req.review_title, req.comment, now))
    
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Review submitted with 'Verified Purchase' badge."}


# ----------------- 11. AI FRAUD DETECTION & DEMAND FORECASTING -----------------

@app.post("/api/fraud-check", summary="Run AI Authenticity & Fraud Risk Inspection")
def api_fraud_check(p: Dict[str, Any]):
    res = check_product_authenticity_and_fraud(
        title=p.get("title", "Handloom Item"),
        craft_type=p.get("craft_type", "Handloom"),
        region=p.get("state_cluster", "Maharashtra"),
        material_cost=float(p.get("material_cost", 500)),
        selling_price=float(p.get("selling_price", 2000)),
        image_url=p.get("image_url", "")
    )
    return {"status": "success", "data": res}


@app.get("/api/demand-forecasts", summary="Get AI Craft Demand Forecasts")
def api_demand_forecasts():
    res = get_craft_demand_forecasts()
    return {"status": "success", "data": res}


# ----------------- 12. NOTIFICATIONS & AUDIT LOG -----------------

@app.get("/api/notifications", summary="Get In-App Notifications")
def api_get_notifications(role: Optional[str] = "ARTISAN"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications WHERE recipient_role = ? ORDER BY id DESC LIMIT 20", (role.upper(),))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return {"status": "success", "data": rows}


@app.get("/api/admin/metrics", summary="Get Admin Ecosystem Metrics")
def api_admin_metrics():
    res = get_admin_dashboard_metrics()
    return {"status": "success", "data": res}


@app.post("/api/admin/review-artisan", summary="Admin Approve/Reject Artisan Application")
def api_admin_review_artisan(payload: Dict[str, Any]):
    artisan_id = int(payload.get("artisan_id", 1))
    action = payload.get("action", "approve")
    admin_name = payload.get("admin_name", "SIH Admin")
    notes = payload.get("notes", "")
    res = admin_review_artisan(artisan_id, action, admin_name, notes)
    return {"status": "success", "data": res}


@app.get("/api/admin/audit-logs", summary="Get Admin Action Audit Log")
def api_admin_audit_logs():
    res = get_admin_audit_logs()
    return {"status": "success", "data": res}


# ----------------- 13. ONDC BECKN PROTOCOL INSPECTOR -----------------

@app.post("/api/export-ondc", summary="Export Beckn JSON-LD Discovery Schema")
def api_export_ondc(payload: Dict[str, Any]):
    craft_data = payload.get("craft_data", {})
    artisan_name = payload.get("artisan_name", "Savita Tai")
    region = payload.get("artisan_region", "Maharashtra")
    res = export_to_beckn_ondc_catalog(craft_data, artisan_name, region)
    return {"status": "success", "data": res}


@app.post("/api/export-ondc-flow", summary="Generate Beckn Protocol Flow Step Payload")
def api_export_ondc_flow(payload: Dict[str, Any]):
    step_name = payload.get("step_name", "search")
    order_data = payload.get("order_data", {})
    res = generate_beckn_flow_step(step_name, order_data)
    return {"status": "success", "data": res}


# ----------------- 14. STATIC ASSETS & SINGLE PAGE APP -----------------

base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(base_dir, "frontend")

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def serve_home():
        return FileResponse(os.path.join(frontend_path, "index.html"))

    # Support client routing catch-all
    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API route not found")
        return FileResponse(os.path.join(frontend_path, "index.html"))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"\n🚀 AI Artisan Commerce Network Server starting at http://0.0.0.0:{port}\n")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
