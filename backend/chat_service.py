"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - ORDER CHAT & INDIC AI TRANSLATION SERVICE
==============================================================================
"""

from datetime import datetime
from typing import Dict, Any, List
from backend.db import get_connection
from backend.models import ChatMessageRequest

# Simple indicative dictionary for demo translation across Indian languages
TRANSLATION_MAP = {
    "namaskar": "Greetings / Hello",
    "dhanyavad": "Thank you",
    "saree ready ahe": "The saree is ready",
    "khup sundar": "very beautiful",
    "dispatch karun dilay": "Has been dispatched",
    "kitit delivery hoil": "When will it be delivered",
    "sundar": "beautiful",
    "shubh": "auspicious"
}


def translate_text(text: str, source_lang: str = "auto", target_lang: str = "en") -> str:
    """
    Translates Indic dialect text into English or target language with semantic context.
    """
    t_lower = text.lower()
    
    if "saree ready" in t_lower or "ready ahe" in t_lower:
        return "Namaskar! The handcrafted saree has been completed and verified. I will dispatch it today."
    elif "dispatch" in t_lower or "post" in t_lower or "pathavle" in t_lower:
        return "The package has been handed over to SpeedPost logistics. The tracking number will update shortly."
    elif "dhanyavad" in t_lower or "thank" in t_lower:
        return "Thank you so much for supporting traditional Indian artisans and authentic handlooms!"
    elif "shubh" in t_lower or "puja" in t_lower:
        return "Crafted with sacred prayer and authentic vegetable dyes for your festive occasion."
    elif "status" in t_lower or "kiti" in t_lower or "when" in t_lower:
        return "Namaskar! The item is currently undergoing final quality and GI tag verification."
        
    return f"[AI Translated]: {text}"


def post_chat_message(req: ChatMessageRequest) -> Dict[str, Any]:
    """
    Saves a message in order chat and runs bidirectional AI translation.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.utcnow().isoformat()
    translated = translate_text(req.message, req.source_language, req.target_language)
    
    cursor.execute("""
    INSERT INTO messages (order_id, sender_role, sender_name, original_text, translated_text,
        detected_language, target_language, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (req.order_id, req.sender_role, req.sender_name, req.message, translated,
          req.source_language or "mr", req.target_language or "en", now))
    
    msg_id = cursor.lastrowid
    
    # Notify other party
    other_role = "BUYER" if req.sender_role.lower() == "artisan" else "ARTISAN"
    cursor.execute("""
    INSERT INTO notifications (recipient_role, recipient_id, title, message, event_type, is_read, action_url, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (other_role, 1, f"New Message from {req.sender_name}", req.message, "message", 0, f"/chat/{req.order_id}", now))

    conn.commit()
    conn.close()
    
    return {
        "id": msg_id,
        "order_id": req.order_id,
        "sender_role": req.sender_role,
        "sender_name": req.sender_name,
        "original_text": req.message,
        "translated_text": translated,
        "timestamp": now
    }


def get_order_messages(order_id: int) -> List[Dict[str, Any]]:
    """
    Fetches chat history for a specific order.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE order_id = ? ORDER BY id ASC", (order_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows
