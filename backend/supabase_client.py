"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - SUPABASE DATABASE & STORE CLIENT
==============================================================================
"""

import os
from datetime import datetime
from typing import Dict, Any, List, Optional

# Initial Seed Listings so Marketplace is never empty
_INITIAL_SEEDS = [
    {
        "id": 1,
        "artisan_name": "Savita Tai (Master Weaver)",
        "state_cluster": "Maharashtra",
        "craft_title": "Authentic Handwoven Paithani Silk Saree",
        "category": "Handloom & Silk",
        "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&auto=format&fit=crop&q=80",
        "material_cost": 800.0,
        "labor_hours": 15.0,
        "suggested_fair_price": 2344.0,
        "hourly_wage_rate": 65.0,
        "heritage_story": "Handcrafted in Yeola cluster with pure mulberry silk and golden zari peacock motifs over 15 painstaking hours.",
        "tags": ["Handloom", "Pure Silk", "GI-Protected", "Fair Wage Guaranteed"],
        "whatsapp_contact": "919876543210",
        "created_at": datetime.utcnow().isoformat()
    },
    {
        "id": 2,
        "artisan_name": "Sunita Devi (Folk Artist)",
        "state_cluster": "Bihar",
        "craft_title": "Traditional Madhubani Mithila Painting",
        "category": "Folk Art & Wall Decor",
        "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=600&auto=format&fit=crop&q=80",
        "material_cost": 350.0,
        "labor_hours": 8.0,
        "suggested_fair_price": 1220.0,
        "hourly_wage_rate": 62.0,
        "heritage_story": "Mithila folk art on handmade paper depicting Tree of Life and sacred fish using natural vegetable extracts.",
        "tags": ["Folk Art", "Natural Dyes", "Mithila GI", "Fair Wage Guaranteed"],
        "whatsapp_contact": "919876543211",
        "created_at": datetime.utcnow().isoformat()
    },
    {
        "id": 3,
        "artisan_name": "Rameshwar Prajapat",
        "state_cluster": "Rajasthan",
        "craft_title": "Jaipur Blue Pottery Floral Vase",
        "category": "Ceramics & Decor",
        "image_url": "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=600&auto=format&fit=crop&q=80",
        "material_cost": 200.0,
        "labor_hours": 5.0,
        "suggested_fair_price": 815.0,
        "hourly_wage_rate": 65.0,
        "heritage_story": "Traditional Jaipur blue pottery made with quartz stone powder without clay, fired with lead-free glaze.",
        "tags": ["Ceramics", "No-Clay Quartz", "Jaipur GI", "Fair Wage Guaranteed"],
        "whatsapp_contact": "919876543212",
        "created_at": datetime.utcnow().isoformat()
    },
    {
        "id": 4,
        "artisan_name": "Somnath Baghel (Tribal Master)",
        "state_cluster": "Odisha",
        "craft_title": "Tribal Dhokra Lost-Wax Bell Metal Figurine",
        "category": "Metallurgy & Sculpture",
        "image_url": "https://images.unsplash.com/photo-1567825836480-4c379a5840ca?w=600&auto=format&fit=crop&q=80",
        "material_cost": 600.0,
        "labor_hours": 18.0,
        "suggested_fair_price": 2425.0,
        "hourly_wage_rate": 60.0,
        "heritage_story": "Prehistoric lost-wax cast bell metal brass tribal dancing figurine crafted using 4000-year ancient metallurgy.",
        "tags": ["Bell Metal", "Lost-Wax Cast", "Tribal GI", "Fair Wage Guaranteed"],
        "whatsapp_contact": "919876543213",
        "created_at": datetime.utcnow().isoformat()
    }
]

_local_listings_db: List[Dict[str, Any]] = list(_INITIAL_SEEDS)
_local_orders_db: List[Dict[str, Any]] = []


def get_supabase_client():
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        return None

    try:
        from supabase import create_client
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"⚠️ Supabase client note: {e}")
        return None


def save_craft_listing(listing: Dict[str, Any]) -> Dict[str, Any]:
    """
    Saves an artisan craft listing to Supabase (or memory fallback).
    """
    new_id = len(_local_listings_db) + 100
    record = {
        "id": new_id,
        "artisan_name": listing.get("artisan_name", "Anonymous Master Artisan"),
        "state_cluster": listing.get("state_cluster", "Maharashtra"),
        "craft_title": listing.get("craft_title", "Handmade Craft"),
        "category": listing.get("category", "Handicrafts"),
        "image_url": listing.get("image_url") or "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&auto=format&fit=crop&q=80",
        "material_cost": float(listing.get("material_cost", 0)),
        "labor_hours": float(listing.get("labor_hours", 0)),
        "suggested_fair_price": float(listing.get("suggested_fair_price", 0)),
        "hourly_wage_rate": float(listing.get("hourly_wage_rate", 65.0)),
        "heritage_story": listing.get("heritage_story", ""),
        "tags": listing.get("tags", []),
        "whatsapp_contact": listing.get("whatsapp_contact", "919876543210"),
        "ondc_schema": listing.get("ondc_schema", {}),
        "created_at": datetime.utcnow().isoformat()
    }

    client = get_supabase_client()
    if client:
        try:
            res = client.table("craft_listings").insert(record).execute()
            if res.data:
                return res.data[0]
        except Exception as e:
            print(f"⚠️ Supabase insert fallback: {e}")

    # Fallback to local memory
    _local_listings_db.insert(0, record)
    return record


def get_all_craft_listings() -> List[Dict[str, Any]]:
    """
    Fetches all available craft listings for buyer marketplace.
    """
    client = get_supabase_client()
    if client:
        try:
            res = client.table("craft_listings").select("*").order("created_at", desc=True).limit(50).execute()
            if res.data and len(res.data) > 0:
                return res.data
        except Exception as e:
            print(f"⚠️ Supabase fetch fallback: {e}")

    return _local_listings_db


def delete_craft_listing(listing_id: int) -> Dict[str, Any]:
    """
    Removes/unlists a craft item from Supabase and local cache.
    """
    global _local_listings_db
    client = get_supabase_client()
    if client:
        try:
            client.table("craft_listings").delete().eq("id", listing_id).execute()
        except Exception as e:
            print(f"⚠️ Supabase delete error: {e}")

    _local_listings_db = [item for item in _local_listings_db if item.get("id") != listing_id]
    return {"status": "success", "deleted_id": listing_id}


def create_order_record(order: Dict[str, Any]) -> Dict[str, Any]:
    """
    Records a completed direct buyer order with transparent wage breakdown.
    """
    order_id = f"ORD-{int(datetime.utcnow().timestamp())}"
    record = {
        "order_id": order_id,
        "craft_id": order.get("craft_id"),
        "craft_title": order.get("craft_title"),
        "artisan_name": order.get("artisan_name"),
        "buyer_name": order.get("buyer_name", "Anonymous Buyer"),
        "buyer_phone": order.get("buyer_phone", ""),
        "delivery_city": order.get("delivery_city", "Bengaluru"),
        "total_amount": float(order.get("total_amount", 0)),
        "artisan_wage_payout": float(order.get("artisan_wage_payout", 0)),
        "status": "PAID_ESCROW_INITIATED",
        "created_at": datetime.utcnow().isoformat()
    }

    client = get_supabase_client()
    if client:
        try:
            res = client.table("orders").insert(record).execute()
            if res.data:
                return res.data[0]
        except Exception as e:
            print(f"⚠️ Supabase order note: {e}")

    _local_orders_db.insert(0, record)
    return record
