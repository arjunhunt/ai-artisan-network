"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - UNIFIED DATABASE MANAGER (SQLITE + SUPABASE SYNC)
==============================================================================
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "artisan_network.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL, -- ARTISAN, BUYER, ADMIN
        name TEXT NOT NULL,
        identifier TEXT UNIQUE NOT NULL, -- mobile or email or username
        email TEXT,
        mobile TEXT,
        state TEXT,
        district TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 2. Artisans Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artisans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        profile_photo TEXT,
        state_cluster TEXT NOT NULL,
        district TEXT,
        village_city TEXT,
        craft_category TEXT NOT NULL,
        specific_craft TEXT NOT NULL,
        years_experience INTEGER DEFAULT 5,
        languages TEXT, -- JSON array
        vishwakarma_id TEXT,
        gi_association TEXT,
        cooperative_association TEXT,
        verification_status TEXT DEFAULT 'PENDING', -- UNVERIFIED, PENDING, VERIFIED, REJECTED
        verification_notes TEXT,
        bank_masked TEXT DEFAULT '••••••••4821',
        rating REAL DEFAULT 4.9,
        verified_orders_count INTEGER DEFAULT 0,
        story TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 3. Buyers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buyers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        mobile TEXT,
        email TEXT,
        default_address TEXT,
        default_pincode TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 4. Wage Rules Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wage_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state_name TEXT NOT NULL,
        craft_name TEXT NOT NULL,
        skill_level TEXT DEFAULT 'Skilled',
        daily_wage REAL NOT NULL,
        hourly_rate REAL NOT NULL,
        effective_date TEXT NOT NULL,
        statutory_reference TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # 5. GI Records (Geographical Indications Registry)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gi_number TEXT UNIQUE NOT NULL,
        craft_name TEXT NOT NULL,
        region_state TEXT NOT NULL,
        category TEXT NOT NULL,
        authorized_association TEXT NOT NULL,
        registered_year INTEGER,
        status TEXT DEFAULT 'VERIFIED',
        certificate_url TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 6. Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artisan_id INTEGER,
        artisan_name TEXT NOT NULL,
        title TEXT NOT NULL,
        short_description TEXT,
        description TEXT,
        heritage_story TEXT,
        category TEXT NOT NULL,
        craft_type TEXT NOT NULL,
        state_cluster TEXT NOT NULL,
        materials TEXT, -- JSON array
        technique TEXT,
        motifs TEXT, -- JSON array
        dimensions TEXT,
        weight TEXT,
        care_instructions TEXT,
        image_urls TEXT, -- JSON array
        material_cost REAL NOT NULL,
        labor_hours REAL NOT NULL,
        hourly_wage_rate REAL NOT NULL,
        suggested_fair_price REAL NOT NULL,
        selling_price REAL NOT NULL,
        stock_quantity INTEGER DEFAULT 1,
        is_made_to_order INTEGER DEFAULT 0,
        production_days INTEGER DEFAULT 3,
        gi_number TEXT,
        gi_verified INTEGER DEFAULT 0,
        tags TEXT, -- JSON array
        status TEXT DEFAULT 'PUBLISHED', -- DRAFT, PENDING_VERIFICATION, VERIFIED, PUBLISHED, SOLD_OUT, ARCHIVED
        view_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    # 7. Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        product_id INTEGER NOT NULL,
        product_title TEXT NOT NULL,
        product_image TEXT,
        artisan_id INTEGER,
        artisan_name TEXT NOT NULL,
        buyer_id INTEGER,
        buyer_name TEXT NOT NULL,
        buyer_phone TEXT NOT NULL,
        delivery_address TEXT NOT NULL,
        delivery_pincode TEXT NOT NULL,
        delivery_city TEXT NOT NULL,
        delivery_state TEXT NOT NULL,
        quantity INTEGER DEFAULT 1,
        unit_price REAL NOT NULL,
        total_amount REAL NOT NULL,
        artisan_wage_payout REAL NOT NULL,
        raw_material_payout REAL NOT NULL,
        logistics_fee REAL NOT NULL,
        platform_fee REAL NOT NULL,
        payment_method TEXT DEFAULT 'DEMO_UPI_ESCROW',
        payment_status TEXT DEFAULT 'AUTHORIZED',
        escrow_state TEXT DEFAULT 'PAYMENT_SECURED',
        carrier TEXT DEFAULT 'India Post SpeedPost (ONDC Logistics)',
        tracking_number TEXT,
        estimated_delivery TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    # 8. Escrow Records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS escrow_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        order_number TEXT NOT NULL,
        total_held REAL NOT NULL,
        artisan_share REAL NOT NULL,
        platform_share REAL NOT NULL,
        status TEXT DEFAULT 'HELD', -- HELD, RELEASED, REFUNDED, DISPUTED
        held_at TEXT NOT NULL,
        released_at TEXT,
        release_tx_ref TEXT
    )
    """)

    # 9. Tracking Events
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracking_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        status_key TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        location TEXT,
        timestamp TEXT NOT NULL
    )
    """)

    # 10. Messages (Artisan <-> Buyer Chat)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        sender_role TEXT NOT NULL, -- artisan / buyer
        sender_name TEXT NOT NULL,
        original_text TEXT NOT NULL,
        translated_text TEXT,
        detected_language TEXT DEFAULT 'mr',
        target_language TEXT DEFAULT 'en',
        timestamp TEXT NOT NULL
    )
    """)

    # 11. Notifications
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipient_role TEXT NOT NULL, -- ARTISAN, BUYER, ADMIN
        recipient_id INTEGER,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        event_type TEXT NOT NULL, -- order, escrow, verification, message, dispute
        is_read INTEGER DEFAULT 0,
        action_url TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 12. Reviews
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        order_id INTEGER,
        buyer_name TEXT NOT NULL,
        is_verified_purchase INTEGER DEFAULT 1,
        rating INTEGER NOT NULL,
        review_title TEXT,
        comment TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # 13. Admin Action Audit Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_name TEXT NOT NULL,
        action_type TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        previous_state TEXT,
        new_state TEXT,
        reason TEXT,
        timestamp TEXT NOT NULL
    )
    """)

    # 14. Demand Forecasts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS demand_forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        craft_category TEXT NOT NULL,
        region TEXT NOT NULL,
        expected_demand_growth_pct REAL NOT NULL,
        suggested_extra_units INTEGER NOT NULL,
        reasons TEXT, -- JSON array
        upcoming_festivals TEXT, -- JSON array
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# Ensure DB initialized at import
init_db()
