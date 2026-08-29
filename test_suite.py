import urllib.request
import json
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = "http://localhost:8000"

def post_json(endpoint, data):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def get_json(endpoint):
    with urllib.request.urlopen(f"{BASE_URL}{endpoint}") as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

print("--- RUNNING SUITE OF VERIFICATION TESTS ---")

# 1. Test Products
status, res = get_json("/api/products")
print(f"1. Products endpoint: HTTP {status}, Found {len(res['data'])} products.")
assert status == 200 and len(res["data"]) > 0

# 2. Test Voice NLP Analysis
status, res = post_json("/api/analyze-craft", {
    "voice_transcript": "Ye hamne pure mulberry silk aur golden zari se banaya hai. Peacock mor motif weave karne me 15 ghante lage.",
    "artisan_name": "Rishikant Mishra",
    "artisan_region": "Maharashtra"
})
print(f"2. Voice NLP: HTTP {status}, Detected: {res['data']['detected_craft_title']}, Confidence: {res['data']['confidence_score']}")
assert status == 200 and "Paithani" in res["data"]["detected_craft_title"]

# 3. Test Fair Pricing Math & Underpricing Defense
status, res = post_json("/api/calculate-price", {
    "material_cost": 800.0,
    "labor_hours": 15.0,
    "state_name": "Maharashtra",
    "artisan_intended_price": 900.0
})
print(f"3. Price Engine: HTTP {status}, Suggested: Rs. {res['data']['fair_selling_price']}, Warning: {res['data']['underpricing_warning']}")
assert status == 200 and res["data"]["underpricing_warning"] is True

# 4. Test GI Verification
status, res = post_json("/api/gi/verify", {
    "gi_number": "GI-MH-001",
    "craft": "Paithani",
    "region": "Maharashtra",
    "artisan_name": "Rishikant Mishra"
})
print(f"4. GI Verification: HTTP {status}, Status: {res['data']['status']}, Verified: {res['data']['verified']}")
assert status == 200 and res["data"]["verified"] is True

# 5. Test Logistics Pincode Check
status, res = post_json("/api/logistics/check-pincode", {"pincode": "560103"})
print(f"5. Pincode Check: HTTP {status}, Serviceable: {res['data']['serviceable']}, Carrier: {res['data']['carrier']}")
assert status == 200 and res["data"]["serviceable"] is True

# 6. Test Order Creation & Escrow Lock
status, res = post_json("/api/orders", {
    "product_id": 1,
    "quantity": 1,
    "buyer_name": "Rajesh Kumar",
    "buyer_phone": "+91 98111 22334",
    "delivery_address": "Flat 402, Green Glen Layout, Bellandur",
    "delivery_pincode": "560103",
    "delivery_city": "Bengaluru",
    "delivery_state": "Karnataka"
})
order_id = res["order_id"]
print(f"6. Order Creation: HTTP {status}, Order #{res['order_number']}, Escrow Locked: Rs. {res['artisan_wage_secured']}")
assert status == 200 and res["escrow_state"] == "PAYMENT_SECURED"

# 7. Test Escrow State Machine Transition
status, res = post_json("/api/orders/transition", {
    "order_id": order_id,
    "new_state": "CRAFTING",
    "note": "Artisan started pitloom weaving.",
    "actor": "artisan"
})
print(f"7. Escrow Transition: HTTP {status}, New State: {res['data']['new_state']}")
assert status == 200 and res["data"]["new_state"] == "CRAFTING"

# 8. Test Chat with AI Translation
status, res = post_json("/api/chat/messages", {
    "order_id": order_id,
    "sender_role": "artisan",
    "sender_name": "Rishikant Mishra",
    "message": "Saree ready ahe, dispatch karun dilay."
})
print(f"8. Chat Translation: HTTP {status}, Original: '{res['data']['original_text']}' -> Translated: '{res['data']['translated_text']}'")
assert status == 200 and res["data"]["translated_text"] != ""

# 9. Test Admin Dashboard Metrics
status, res = get_json("/api/admin/metrics")
print(f"9. Admin Metrics: HTTP {status}, Total Artisans: {res['data']['total_artisans']}, Escrow Held: Rs. {res['data']['active_escrow_held_inr']}")
assert status == 200 and res["data"]["total_artisans"] > 0

# 10. Test ONDC Beckn Export
status, res = post_json("/api/export-ondc", {
    "craft_data": {"title": "Paithani Saree", "selling_price": 2344.0},
    "artisan_name": "Rishikant Mishra",
    "artisan_region": "Maharashtra"
})
print(f"10. ONDC Beckn Schema: HTTP {status}, Context Action: {res['data']['context']['action']}")
assert status == 200 and res["data"]["context"]["action"] == "on_search"

print("\n🎉 ALL 10 VERIFICATION TESTS PASSED PERFECTLY!")
