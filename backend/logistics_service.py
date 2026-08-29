"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - LOGISTICS & PINCODE SERVICE
==============================================================================
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Any, List
from backend.db import get_connection

# State lookup by Pincode Prefix (India Post standard)
PINCODE_PREFIX_MAP = {
    "11": ("Delhi", "North Zone", 100.0, 2),
    "12": ("Haryana", "North Zone", 100.0, 2),
    "13": ("Haryana", "North Zone", 100.0, 2),
    "14": ("Punjab", "North Zone", 120.0, 3),
    "18": ("Jammu & Kashmir", "North Zone", 160.0, 4),
    "19": ("Jammu & Kashmir", "North Zone", 160.0, 4),
    "20": ("Uttar Pradesh", "North Zone", 120.0, 3),
    "22": ("Uttar Pradesh", "North Zone", 120.0, 3),
    "30": ("Rajasthan", "West Zone", 120.0, 3),
    "31": ("Rajasthan", "West Zone", 120.0, 3),
    "36": ("Gujarat", "West Zone", 130.0, 3),
    "38": ("Gujarat", "West Zone", 130.0, 3),
    "40": ("Maharashtra", "West Zone", 100.0, 2),
    "41": ("Maharashtra", "West Zone", 100.0, 2),
    "42": ("Maharashtra", "West Zone", 100.0, 2),
    "43": ("Maharashtra", "West Zone", 100.0, 2),
    "44": ("Maharashtra", "West Zone", 100.0, 2),
    "50": ("Telangana", "South Zone", 130.0, 3),
    "56": ("Karnataka", "South Zone", 120.0, 2),
    "57": ("Karnataka", "South Zone", 120.0, 2),
    "60": ("Tamil Nadu", "South Zone", 130.0, 3),
    "62": ("Tamil Nadu", "South Zone", 130.0, 3),
    "68": ("Kerala", "South Zone", 140.0, 3),
    "70": ("West Bengal", "East Zone", 140.0, 3),
    "75": ("Odisha", "East Zone", 140.0, 3),
    "78": ("Assam", "North East Zone", 180.0, 5),
    "80": ("Bihar", "East Zone", 130.0, 3),
    "84": ("Bihar", "East Zone", 130.0, 3)
}


def check_pincode_serviceability(pincode: str) -> Dict[str, Any]:
    """
    Checks if an Indian pincode is serviceable via ONDC India Post / Courier network.
    """
    pincode_clean = re.sub(r"\D", "", pincode.strip())
    
    if len(pincode_clean) != 6:
        return {
            "serviceable": False,
            "pincode": pincode,
            "message": "Invalid Indian postal PIN code format (must be 6 digits)."
        }
        
    prefix = pincode_clean[:2]
    lookup = PINCODE_PREFIX_MAP.get(prefix, ("Pan-India Delivery Hub", "Standard Postal Zone", 150.0, 4))
    
    state, zone, shipping_cost, delivery_days = lookup
    est_date = (datetime.utcnow() + timedelta(days=delivery_days)).strftime("%A, %d %B %Y")
    
    return {
        "serviceable": True,
        "pincode": pincode_clean,
        "state": state,
        "postal_zone": zone,
        "shipping_cost": shipping_cost,
        "estimated_days": delivery_days,
        "estimated_delivery_date": est_date,
        "carrier": "India Post SpeedPost (ONDC Logistics Adapter)",
        "cash_on_delivery": False,
        "escrow_supported": True,
        "message": f"Serviceable via SpeedPost. Estimated delivery by {est_date}."
    }


def get_order_tracking_timeline(order_id: int) -> List[Dict[str, Any]]:
    """
    Retrieves full event-based chronological tracking timeline for an order.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM tracking_events
    WHERE order_id = ?
    ORDER BY id ASC
    """, (order_id,))
    
    events = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return events
