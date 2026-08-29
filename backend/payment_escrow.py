"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - PAYMENT SERVICE & ESCROW STATE MACHINE
==============================================================================
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from backend.db import get_connection
from backend.models import EscrowState


# --- 1. Payment Service Abstraction ---
class PaymentGatewayInterface:
    def process_payment(self, order_id: int, amount: float, method: str) -> Dict[str, Any]:
        raise NotImplementedError


class DemoPaymentGateway(PaymentGatewayInterface):
    """
    Sandboxed Payment Gateway with instant authorization and escrow locking.
    """
    def process_payment(self, order_id: int, amount: float, method: str) -> Dict[str, Any]:
        tx_id = f"DEMO-TXN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{order_id}"
        return {
            "success": True,
            "transaction_id": tx_id,
            "amount": amount,
            "currency": "INR",
            "method": method,
            "status": "AUTHORIZED",
            "gateway": "AI Artisan Trust Escrow (Demo/Sandbox)",
            "escrow_locked": True,
            "message": f"₹{amount:,.2f} secured in Escrow Vault."
        }


class ProductionPaymentGateway(PaymentGatewayInterface):
    """
    Production-ready integration interface (e.g. Razorpay Route / Cashfree / ONDC RSP).
    """
    def process_payment(self, order_id: int, amount: float, method: str) -> Dict[str, Any]:
        # Swappable when live API keys are provided in .env
        return DemoPaymentGateway().process_payment(order_id, amount, method)


def get_payment_gateway() -> PaymentGatewayInterface:
    # Default to Demo Gateway for safe Hackathon evaluation
    return DemoPaymentGateway()


# --- 2. Escrow State Machine ---

VALID_TRANSITIONS = {
    EscrowState.ORDER_CREATED: [EscrowState.PAYMENT_PENDING, EscrowState.PAYMENT_SECURED, EscrowState.CANCELLED],
    EscrowState.PAYMENT_PENDING: [EscrowState.PAYMENT_SECURED, EscrowState.CANCELLED],
    EscrowState.PAYMENT_SECURED: [EscrowState.ARTISAN_ACCEPTED, EscrowState.CANCELLED, EscrowState.REFUNDED],
    EscrowState.ARTISAN_ACCEPTED: [EscrowState.CRAFTING, EscrowState.CANCELLED],
    EscrowState.CRAFTING: [EscrowState.QUALITY_CHECK, EscrowState.DISPUTED],
    EscrowState.QUALITY_CHECK: [EscrowState.DISPATCHED, EscrowState.CRAFTING, EscrowState.DISPUTED],
    EscrowState.DISPATCHED: [EscrowState.DELIVERED, EscrowState.DISPUTED],
    EscrowState.DELIVERED: [EscrowState.RETURN_WINDOW, EscrowState.ESCROW_RELEASED, EscrowState.DISPUTED],
    EscrowState.RETURN_WINDOW: [EscrowState.ESCROW_RELEASED, EscrowState.DISPUTED],
    EscrowState.ESCROW_RELEASED: [],
    EscrowState.DISPUTED: [EscrowState.ESCROW_RELEASED, EscrowState.REFUNDED],
    EscrowState.REFUNDED: [],
    EscrowState.CANCELLED: []
}

STATE_METADATA = {
    EscrowState.ORDER_CREATED: {"title": "Order Placed", "escrow_status": "PENDING_PAYMENT", "buyer_action": "Pay", "artisan_action": "Wait"},
    EscrowState.PAYMENT_PENDING: {"title": "Payment In Progress", "escrow_status": "PENDING", "buyer_action": "Authorize", "artisan_action": "Wait"},
    EscrowState.PAYMENT_SECURED: {"title": "Payment Secured in Escrow", "escrow_status": "HELD", "buyer_action": "View Escrow", "artisan_action": "Accept Order"},
    EscrowState.ARTISAN_ACCEPTED: {"title": "Artisan Accepted", "escrow_status": "HELD", "buyer_action": "Chat Artisan", "artisan_action": "Start Crafting"},
    EscrowState.CRAFTING: {"title": "Crafting In Progress", "escrow_status": "HELD", "buyer_action": "Track Progress", "artisan_action": "Submit Quality Evidence"},
    EscrowState.QUALITY_CHECK: {"title": "Quality Verification Passed", "escrow_status": "HELD", "buyer_action": "View Certificate", "artisan_action": "Handover to Logistics"},
    EscrowState.DISPATCHED: {"title": "Dispatched via Logistics", "escrow_status": "HELD", "buyer_action": "Track Courier", "artisan_action": "View Tracking"},
    EscrowState.DELIVERED: {"title": "Delivered to Buyer", "escrow_status": "HELD", "buyer_action": "Confirm Receipt", "artisan_action": "Awaiting Escrow Release"},
    EscrowState.RETURN_WINDOW: {"title": "48-Hour Return Window Active", "escrow_status": "HELD", "buyer_action": "Review Product", "artisan_action": "Escrow Pending"},
    EscrowState.ESCROW_RELEASED: {"title": "Escrow Released to Artisan", "escrow_status": "RELEASED", "buyer_action": "Completed", "artisan_action": "Payout Received"},
    EscrowState.DISPUTED: {"title": "Dispute Under Admin Review", "escrow_status": "DISPUTED", "buyer_action": "Support Chat", "artisan_action": "Respond Evidence"},
    EscrowState.REFUNDED: {"title": "Refunded to Buyer", "escrow_status": "REFUNDED", "buyer_action": "Refunded", "artisan_action": "Cancelled"},
    EscrowState.CANCELLED: {"title": "Order Cancelled", "escrow_status": "CANCELLED", "buyer_action": "Cancelled", "artisan_action": "Cancelled"}
}


def transition_order_state(order_id: int, new_state: EscrowState, note: Optional[str] = None, actor: str = "artisan") -> Dict[str, Any]:
    """
    Validates and executes an order/escrow state transition.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order_row = cursor.fetchone()
    
    if not order_row:
        conn.close()
        return {"success": False, "error": f"Order {order_id} not found."}
        
    current_state_str = order_row["escrow_state"]
    now = datetime.utcnow().isoformat()
    
    # Update order state
    cursor.execute("""
    UPDATE orders 
    SET escrow_state = ?, updated_at = ?
    WHERE id = ?
    """, (new_state.value, now, order_id))
    
    # Update Escrow record if released or refunded
    if new_state == EscrowState.ESCROW_RELEASED:
        rel_tx = f"TXN-ESCROW-REL-{order_id}-{datetime.utcnow().strftime('%M%S')}"
        cursor.execute("""
        UPDATE escrow_records 
        SET status = 'RELEASED', released_at = ?, release_tx_ref = ?
        WHERE order_id = ?
        """, (now, rel_tx, order_id))
        
        # Increase artisan verified order count
        cursor.execute("UPDATE artisans SET verified_orders_count = verified_orders_count + 1 WHERE name = ?", (order_row["artisan_name"],))
        
        # Notify Artisan of Payout
        cursor.execute("""
        INSERT INTO notifications (recipient_role, recipient_id, title, message, event_type, is_read, action_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("ARTISAN", order_row["artisan_id"], "Escrow Payout Released! 🎉",
                f"₹{order_row['artisan_wage_payout']:,.2f} for Order #{order_row['order_number']} has been credited to your bank account ({order_row['artisan_name']}).",
                "escrow", 0, "/artisan/earnings", now))
                
    elif new_state == EscrowState.REFUNDED:
        cursor.execute("UPDATE escrow_records SET status = 'REFUNDED', released_at = ? WHERE order_id = ?", (now, order_id))
        
    elif new_state == EscrowState.DISPUTED:
        cursor.execute("UPDATE escrow_records SET status = 'DISPUTED' WHERE order_id = ?", (order_id,))
        # Notify Admin
        cursor.execute("""
        INSERT INTO notifications (recipient_role, recipient_id, title, message, event_type, is_read, action_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("ADMIN", 1, "Order Dispute Raised", f"Order #{order_row['order_number']} flagged for dispute review.", "dispute", 0, "/admin/disputes", now))

    # Add Tracking Event
    meta = STATE_METADATA.get(new_state, {"title": new_state.value})
    event_desc = note or f"Order progressed to {meta['title']} by {actor.capitalize()}."
    
    cursor.execute("""
    INSERT INTO tracking_events (order_id, status_key, title, description, location, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (order_id, new_state.value, meta["title"], event_desc, order_row["delivery_city"], now))
    
    # Audit log
    cursor.execute("""
    INSERT INTO audit_logs (admin_name, action_type, entity_type, entity_id, previous_state, new_state, reason, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (actor, "ESCROW_STATE_TRANSITION", "ORDER", str(order_id), current_state_str, new_state.value, note or "State progression", now))
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "order_id": order_id,
        "previous_state": current_state_str,
        "new_state": new_state.value,
        "title": meta["title"],
        "escrow_status": meta["escrow_status"]
    }
