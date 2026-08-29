"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - ADMIN CONTROL & AUDIT SERVICE
==============================================================================
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.db import get_connection


def get_admin_dashboard_metrics() -> Dict[str, Any]:
    """
    Computes real-time ecosystem stats, GMV, Escrow balance, and pending review counts.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total, SUM(CASE WHEN verification_status='VERIFIED' THEN 1 ELSE 0 END) as verified, SUM(CASE WHEN verification_status='PENDING' THEN 1 ELSE 0 END) as pending FROM artisans")
    artisan_stat = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as total, SUM(view_count) as total_views FROM products")
    prod_stat = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as total_orders, SUM(total_amount) as total_gmv, SUM(artisan_wage_payout) as total_artisan_earnings FROM orders")
    order_stat = cursor.fetchone()

    cursor.execute("SELECT SUM(total_held) as active_escrow FROM escrow_records WHERE status = 'HELD'")
    escrow_stat = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as total_disputes FROM orders WHERE escrow_state = 'DISPUTED'")
    dispute_stat = cursor.fetchone()

    conn.close()

    total_gmv = float(order_stat["total_gmv"] or 0)
    total_earnings = float(order_stat["total_artisan_earnings"] or 0)
    active_escrow = float(escrow_stat["active_escrow"] or 0)

    return {
        "total_artisans": int(artisan_stat["total"] or 0),
        "verified_artisans": int(artisan_stat["verified"] or 0),
        "pending_verifications": int(artisan_stat["pending"] or 0),
        "total_products": int(prod_stat["total"] or 0),
        "total_product_views": int(prod_stat["total_views"] or 0),
        "total_orders": int(order_stat["total_orders"] or 0),
        "gross_merchandise_value_inr": total_gmv,
        "artisan_protected_earnings_inr": total_earnings,
        "active_escrow_held_inr": active_escrow,
        "active_disputes": int(dispute_stat["total_disputes"] or 0),
        "middleman_leakage_prevented_inr": round(total_gmv * 0.42, 2),  # Average 42% middleman margin eliminated
        "languages_supported": 5,
        "is_sandbox_environment": True
    }


def admin_review_artisan(artisan_id: int, action: str, admin_name: str, notes: str = "") -> Dict[str, Any]:
    """
    Approves or rejects an artisan onboarding application and logs the action.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM artisans WHERE id = ?", (artisan_id,))
    artisan = cursor.fetchone()
    if not artisan:
        conn.close()
        return {"success": False, "error": "Artisan not found"}

    prev_status = artisan["verification_status"]
    new_status = "VERIFIED" if action.lower() == "approve" else "REJECTED"
    now = datetime.utcnow().isoformat()

    cursor.execute("""
    UPDATE artisans
    SET verification_status = ?, verification_notes = ?
    WHERE id = ?
    """, (new_status, notes or f"Marked {new_status} by Admin", artisan_id))

    # Add to Audit Log
    cursor.execute("""
    INSERT INTO audit_logs (admin_name, action_type, entity_type, entity_id, previous_state, new_state, reason, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (admin_name, "ARTISAN_VERIFICATION", "ARTISAN", str(artisan_id), prev_status, new_status, notes or action, now))

    # Notify Artisan
    cursor.execute("""
    INSERT INTO notifications (recipient_role, recipient_id, title, message, event_type, is_read, action_url, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("ARTISAN", artisan_id, f"Verification Status: {new_status}", f"Your artisan account has been {new_status.lower()}.", "verification", 0, "/artisan/profile", now))

    conn.commit()
    conn.close()

    return {"success": True, "artisan_id": artisan_id, "new_status": new_status}


def get_admin_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetches the immutable admin audit trail.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows
