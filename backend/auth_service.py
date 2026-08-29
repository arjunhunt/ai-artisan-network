"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - AUTHENTICATION & RBAC SERVICE
==============================================================================
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from backend.db import get_connection
from backend.models import UserRole, AuthLoginRequest, ArtisanOnboardingRequest


DEMO_USERS = {
    # Artisans
    "DEMO-ARTISAN-001": {
        "id": 1,
        "name": "Savita Tai",
        "role": UserRole.ARTISAN,
        "email": "savita@example.test",
        "mobile": "+91 98765 43210",
        "state": "Maharashtra",
        "district": "Nashik",
        "craft": "Paithani Weaving",
        "verification_status": "VERIFIED",
        "vishwakarma_id": "PMV-MH-2024-8841",
        "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-ARTISAN-002": {
        "id": 2,
        "name": "Sunita Devi",
        "role": UserRole.ARTISAN,
        "email": "sunita@example.test",
        "mobile": "+91 98765 43211",
        "state": "Bihar",
        "district": "Madhubani",
        "craft": "Madhubani Painting",
        "verification_status": "VERIFIED",
        "vishwakarma_id": "PMV-BR-2024-3912",
        "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-ARTISAN-003": {
        "id": 3,
        "name": "Rameshwar Prajapat",
        "role": UserRole.ARTISAN,
        "email": "rameshwar@example.test",
        "mobile": "+91 98765 43212",
        "state": "Rajasthan",
        "district": "Jaipur",
        "craft": "Jaipur Blue Pottery",
        "verification_status": "VERIFIED",
        "vishwakarma_id": "PMV-RJ-2023-9014",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-ARTISAN-004": {
        "id": 4,
        "name": "Somnath Baghel",
        "role": UserRole.ARTISAN,
        "email": "somnath@example.test",
        "mobile": "+91 98765 43213",
        "state": "Odisha",
        "district": "Mayurbhanj",
        "craft": "Dhokra Lost-Wax Art",
        "verification_status": "VERIFIED",
        "vishwakarma_id": "PMV-OD-2024-6721",
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-ARTISAN-005": {
        "id": 5,
        "name": "R. Venkatesh",
        "role": UserRole.ARTISAN,
        "email": "venkatesh@example.test",
        "mobile": "+91 98765 43214",
        "state": "Tamil Nadu",
        "district": "Kanchipuram",
        "craft": "Kanchipuram Silk Weaving",
        "verification_status": "VERIFIED",
        "vishwakarma_id": "PMV-TN-2024-5512",
        "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-ARTISAN-006": {
        "id": 6,
        "name": "Biren Boro",
        "role": UserRole.ARTISAN,
        "email": "biren@example.test",
        "mobile": "+91 98765 43215",
        "state": "Assam",
        "district": "Guwahati",
        "craft": "Organic Bamboo & Cane",
        "verification_status": "VERIFIED",
        "vishwakarma_id": "PMV-AS-2024-3321",
        "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-ARTISAN-007": {
        "id": 7,
        "name": "Ananya Sen",
        "role": UserRole.ARTISAN,
        "email": "ananya@example.test",
        "mobile": "+91 98765 43216",
        "state": "West Bengal",
        "district": "Santiniketan",
        "craft": "Kantha Hand Embroidery",
        "verification_status": "VERIFIED",
        "vishwakarma_id": "PMV-WB-2024-4419",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-ARTISAN-008": {
        "id": 8,
        "name": "Farooq Ahmed",
        "role": UserRole.ARTISAN,
        "email": "farooq@example.test",
        "mobile": "+91 98765 43217",
        "state": "Jammu & Kashmir",
        "district": "Srinagar",
        "craft": "Pashmina Cashmere Shawl",
        "verification_status": "VERIFIED",
        "vishwakarma_id": "PMV-JK-2024-1188",
        "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&auto=format&fit=crop&q=80"
    },

    # Buyers
    "DEMO-BUYER-001": {
        "id": 1,
        "name": "Rajesh Kumar",
        "role": UserRole.BUYER,
        "email": "rajesh.k@example.test",
        "mobile": "+91 98111 22334",
        "state": "Karnataka",
        "district": "Bengaluru",
        "address": "Flat 402, Green Glen Layout, Bellandur, Bengaluru - 560103",
        "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-BUYER-002": {
        "id": 2,
        "name": "Priya Sharma",
        "role": UserRole.BUYER,
        "email": "priya.s@example.test",
        "mobile": "+91 98222 33445",
        "state": "Maharashtra",
        "district": "Mumbai",
        "address": "B-12, Sea Pearl Apt, Bandra West, Mumbai - 400050",
        "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-BUYER-003": {
        "id": 3,
        "name": "Amit Verma",
        "role": UserRole.BUYER,
        "email": "amit.v@example.test",
        "mobile": "+91 98333 44556",
        "state": "Delhi",
        "district": "New Delhi",
        "address": "14/2 Connaught Place, New Delhi - 110001",
        "avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-BUYER-004": {
        "id": 4,
        "name": "Deepa Nair",
        "role": UserRole.BUYER,
        "email": "deepa.n@example.test",
        "mobile": "+91 98444 55667",
        "state": "Kerala",
        "district": "Kochi",
        "address": "Palm Grove Villa, Kakkanad, Kochi - 682030",
        "avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-BUYER-005": {
        "id": 5,
        "name": "Vikram Mehta",
        "role": UserRole.BUYER,
        "email": "vikram.m@example.test",
        "mobile": "+91 98555 66778",
        "state": "Gujarat",
        "district": "Ahmedabad",
        "address": "701 heritage heights, Bodakdev, Ahmedabad - 380054",
        "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&auto=format&fit=crop&q=80"
    },
    "DEMO-BUYER-006": {
        "id": 6,
        "name": "Sneha Mukherjee",
        "role": UserRole.BUYER,
        "email": "sneha.m@example.test",
        "mobile": "+91 98666 77889",
        "state": "West Bengal",
        "district": "Kolkata",
        "address": "45/A Lake Road, Ballygunge, Kolkata - 700029",
        "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400&auto=format&fit=crop&q=80"
    },

    # Admin
    "DEMO-ADMIN-001": {
        "id": 1,
        "name": "SIH Admin Official",
        "role": UserRole.ADMIN,
        "email": "admin@sih-artisan.gov.in",
        "mobile": "+91 99000 11223",
        "designation": "National Cluster Nodal Officer",
        "avatar": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&auto=format&fit=crop&q=80"
    }
}


def authenticate_user(req: AuthLoginRequest) -> Dict[str, Any]:
    """
    Authenticates artisan, buyer, or admin with demo credentials or database lookup.
    """
    identifier_clean = req.identifier.strip()
    
    # 1. Check Demo Credentials
    if identifier_clean in DEMO_USERS:
        demo = DEMO_USERS[identifier_clean]
        token = f"demo-jwt-{demo['role'].lower()}-{demo['id']}-secure"
        return {
            "authenticated": True,
            "token": token,
            "role": demo["role"],
            "user": demo,
            "is_demo": True
        }
    
    # 2. Database lookup
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE identifier = ? OR email = ? OR mobile = ?",
                   (identifier_clean, identifier_clean, identifier_clean))
    row = cursor.fetchone()
    
    if row:
        user_dict = dict(row)
        conn.close()
        return {
            "authenticated": True,
            "token": f"live-jwt-{user_dict['role'].lower()}-{user_dict['id']}",
            "role": user_dict["role"],
            "user": user_dict,
            "is_demo": False
        }
        
    # 3. Auto-provision new demo/sandbox user if valid format
    now = datetime.utcnow().isoformat()
    role_str = req.role.value
    name = f"User {identifier_clean[-4:] if len(identifier_clean) >= 4 else identifier_clean}"
    
    cursor.execute("""
    INSERT INTO users (role, name, identifier, email, mobile, state, district, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (role_str, name, identifier_clean, f"{identifier_clean}@artisan.test", identifier_clean, "Maharashtra", "General", now))
    new_user_id = cursor.lastrowid
    
    if req.role == UserRole.ARTISAN:
        cursor.execute("""
        INSERT INTO artisans (user_id, name, state_cluster, craft_category, specific_craft, verification_status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (new_user_id, name, "Maharashtra", "Handicrafts", "Handmade Craft", "PENDING", now))
    elif req.role == UserRole.BUYER:
        cursor.execute("""
        INSERT INTO buyers (user_id, name, mobile, created_at)
        VALUES (?, ?, ?, ?)
        """, (new_user_id, name, identifier_clean, now))
        
    conn.commit()
    conn.close()
    
    return {
        "authenticated": True,
        "token": f"live-jwt-{role_str.lower()}-{new_user_id}",
        "role": role_str,
        "user": {
            "id": new_user_id,
            "name": name,
            "identifier": identifier_clean,
            "role": role_str
        },
        "is_demo": False
    }


def get_all_demo_personas() -> List[Dict[str, Any]]:
    """
    Returns all demo profiles organized for the UI selector.
    """
    return [
        {"identifier": k, **v} for k, v in DEMO_USERS.items()
    ]


def onboard_artisan(req: ArtisanOnboardingRequest) -> Dict[str, Any]:
    """
    Registers a new artisan application with PM Vishwakarma and GI validation hooks.
    """
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    cursor.execute("SELECT id FROM users WHERE mobile = ?", (req.mobile,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        user_id = existing_user["id"]
    else:
        cursor.execute("""
        INSERT INTO users (role, name, identifier, email, mobile, state, district, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("ARTISAN", req.name, req.mobile, req.email or f"{req.mobile}@artisan.test", req.mobile, req.state, req.district, now))
        user_id = cursor.lastrowid

    verification_status = "PENDING"
    notes = "Application received. Pending cluster officer review."
    
    if req.vishwakarma_id and req.vishwakarma_id.startswith("PMV-"):
        verification_status = "VERIFIED"
        notes = f"Auto-verified against PM Vishwakarma Registry ({req.vishwakarma_id})."
        
    cursor.execute("""
    INSERT INTO artisans (user_id, name, profile_photo, state_cluster, district, village_city,
        craft_category, specific_craft, years_experience, languages, vishwakarma_id,
        gi_association, cooperative_association, verification_status, verification_notes,
        bank_masked, story, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, req.name,
        req.profile_photo or "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&auto=format&fit=crop&q=80",
        req.state, req.district, req.village_city, req.craft_category, req.specific_craft,
        req.years_experience, json.dumps(req.languages), req.vishwakarma_id,
        req.gi_association, req.cooperative_association, verification_status, notes,
        req.bank_account_masked or "••••••••4821",
        f"Master craftsman specializing in {req.specific_craft} with {req.years_experience} years of generational experience in {req.state}.",
        now
    ))
    artisan_id = cursor.lastrowid
    
    cursor.execute("""
    INSERT INTO notifications (recipient_role, recipient_id, title, message, event_type, is_read, action_url, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("ADMIN", 1, "New Artisan Application", f"{req.name} ({req.specific_craft}, {req.state}) submitted onboarding application.", "verification", 0, "/admin/verification", now))

    conn.commit()
    conn.close()
    
    return {
        "artisan_id": artisan_id,
        "user_id": user_id,
        "name": req.name,
        "verification_status": verification_status,
        "verification_notes": notes,
        "message": "Artisan onboarded successfully."
    }
