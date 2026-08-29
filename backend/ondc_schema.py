"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - MODULE: ONDC BECKN PROTOCOL GENERATOR
==============================================================================
"""

from datetime import datetime
from typing import Dict, Any, Optional

def export_to_beckn_ondc_catalog(
    product_data: dict,
    artisan_name: str = "Savita Tai",
    region: str = "Maharashtra"
) -> Dict[str, Any]:
    """
    Generates Beckn Protocol JSON-LD catalog schema for ONDC open network discovery.
    """
    now = datetime.utcnow().isoformat()
    
    title = product_data.get("title", "Authentic Handcrafted Artisan Item")
    price = float(product_data.get("suggested_fair_price") or product_data.get("selling_price") or 2344.0)
    category = product_data.get("category", "Handloom & Textiles")
    item_id = str(product_data.get("id", "ITEM-101"))
    
    return {
        "context": {
            "domain": "nic2004:52110",
            "country": "IND",
            "city": "std:080",
            "action": "on_search",
            "core_version": "1.2.0",
            "bap_id": "buyer-app.ondc.org",
            "bap_uri": "https://buyer-app.ondc.org/protocol/v1",
            "bpp_id": "ai-artisan-network.bpp.org",
            "bpp_uri": "https://ai-artisan-network.bpp.org/protocol/v1",
            "transaction_id": f"txn-ondc-{item_id}-{int(datetime.utcnow().timestamp())}",
            "message_id": f"msg-beckn-{item_id}",
            "timestamp": now,
            "ttl": "PT30S"
        },
        "message": {
            "catalog": {
                "bpp/descriptor": {
                    "name": "AI Artisan Commerce Network (BPP)",
                    "short_desc": "Autonomous fair-wage digital enablement layer for rural Indian creators",
                    "images": ["https://ai-artisan-network.vercel.app/static/logo.png"]
                },
                "bpp/providers": [
                    {
                        "id": f"PROVIDER-{region.upper()[:2]}-001",
                        "descriptor": {
                            "name": f"{artisan_name} (Verified Master Artisan)",
                            "short_desc": f"Generational artisan cluster in {region}",
                            "images": [product_data.get("image_url", "")]
                        },
                        "categories": [
                            {
                                "id": f"CAT-{category.replace(' ', '-').upper()}",
                                "descriptor": {"name": category}
                            }
                        ],
                        "items": [
                            {
                                "id": item_id,
                                "descriptor": {
                                    "name": title,
                                    "code": f"GI-{region.upper()[:2]}-CRAFT",
                                    "symbol": product_data.get("image_url", ""),
                                    "short_desc": product_data.get("heritage_story", title),
                                    "images": [product_data.get("image_url", "")]
                                },
                                "price": {
                                    "currency": "INR",
                                    "value": str(price),
                                    "maximum_value": str(round(price * 1.15, 2))
                                },
                                "category_id": f"CAT-{category.replace(' ', '-').upper()}",
                                "fulfillment_id": "FULFILLMENT-SPEEDPOST-ONDC",
                                "location_id": f"LOC-{region.upper()[:2]}",
                                "@ondc/org/returnable": True,
                                "@ondc/org/cancellable": True,
                                "@ondc/org/available_on_cod": False,
                                "@ondc/org/statutory_wage_guarantee": True,
                                "@ondc/org/gi_verified": product_data.get("gi_verified", True),
                                "tags": [
                                    {"code": "fair_pricing", "list": [{"code": "living_wage_escrow", "value": "yes"}]},
                                    {"code": "origin", "list": [{"code": "state", "value": region}]}
                                ]
                            }
                        ]
                    }
                ]
            }
        },
        "is_sandbox_simulation": True
    }


def generate_beckn_flow_step(step_name: str, order_data: dict) -> Dict[str, Any]:
    """
    Generates Beckn protocol payloads for search, select, init, confirm, and status.
    """
    now = datetime.utcnow().isoformat()
    return {
        "step": step_name.lower(),
        "beckn_action": f"/on_{step_name.lower()}",
        "timestamp": now,
        "protocol_version": "1.2.0",
        "payload": {
            "order_id": order_data.get("order_number", "ORD-2026-8819"),
            "state": order_data.get("escrow_state", "PAYMENT_SECURED"),
            "total_value": order_data.get("total_amount", 2344.0),
            "settlement": {
                "type": "ESCROW_SPLIT",
                "artisan_wage": order_data.get("artisan_wage_payout", 975.0),
                "escrow_bank": "AI Artisan Trust Escrow Node"
            }
        }
    }