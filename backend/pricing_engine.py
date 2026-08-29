"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - STATUTORY FAIR PRICING & WAGE ENGINE
==============================================================================
"""

from typing import Dict, Any, Optional
from backend.db import get_connection

# Fallback benchmarks if database is unreachable
FALLBACK_WAGES = {
    "Maharashtra": {"hourly": 65.0, "daily": 520.0, "ref": "MH-MIN-WAGE-SEC-12(A)/2026"},
    "Bihar": {"hourly": 62.0, "daily": 496.0, "ref": "BR-MIN-WAGE-NOTIF-44/2026"},
    "Rajasthan": {"hourly": 65.0, "daily": 520.0, "ref": "RJ-LABOUR-CIRC-881/2026"},
    "Odisha": {"hourly": 60.0, "daily": 480.0, "ref": "OD-TRIBAL-CRAFT-BENCHMARK-03"},
    "Assam": {"hourly": 58.0, "daily": 464.0, "ref": "AS-FOREST-CRAFT-SCALE-09"},
    "Tamil Nadu": {"hourly": 68.0, "daily": 544.0, "ref": "TN-HANDLOOM-WAGE-SCHEDULE-B"},
    "West Bengal": {"hourly": 55.0, "daily": 440.0, "ref": "WB-MIN-WAGE-SCHEDULE-C"},
    "Uttar Pradesh": {"hourly": 55.0, "daily": 440.0, "ref": "UP-LABOUR-MIN-NOTIF-2026"},
    "Karnataka": {"hourly": 65.0, "daily": 520.0, "ref": "KA-MIN-WAGE-2026"},
    "Default": {"hourly": 60.0, "daily": 480.0, "ref": "NATIONAL-FLOOR-WAGE-BENCHMARK"}
}


def get_statutory_wage(state_name: str, craft_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetches the statutory minimum wage rule for a state & craft from SQLite config.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM wage_rules 
    WHERE state_name = ? OR ? LIKE '%' || state_name || '%'
    ORDER BY id DESC LIMIT 1
    """, (state_name, state_name))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "hourly_rate": float(row["hourly_rate"]),
            "daily_wage": float(row["daily_wage"]),
            "skill_level": row["skill_level"],
            "effective_date": row["effective_date"],
            "statutory_reference": row["statutory_reference"],
            "state_name": row["state_name"]
        }
        
    fb = FALLBACK_WAGES.get(state_name, FALLBACK_WAGES["Default"])
    return {
        "hourly_rate": fb["hourly"],
        "daily_wage": fb["daily"],
        "skill_level": "Skilled Artisan",
        "effective_date": "2026-01-01",
        "statutory_reference": fb["ref"],
        "state_name": state_name
    }


def calculate_fair_price(
    material_cost: float,
    labor_hours: float,
    state_name: str = "Maharashtra",
    craft_name: Optional[str] = None,
    skill_level: str = "Skilled",
    desired_margin_pct: float = 20.0,
    packaging_cost: float = 100.0,
    logistics_cost: float = 150.0,
    overhead_cost: float = 100.0,
    artisan_intended_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Computes fair artisan selling price with transparent component breakdowns and underpricing risk alerts.
    Formula:
        Base Production = Material + (Labor Hours * Hourly Wage) + Overheads + Packaging
        Artisan Margin = (Base Production * desired_margin_pct / 100)
        Platform & Logistics = Logistics + (5% Platform maintenance)
        Fair Selling Price = Base Production + Artisan Margin + Logistics + Platform
    """
    wage_info = get_statutory_wage(state_name, craft_name)
    hourly_rate = wage_info["hourly_rate"]
    
    # 1. Statutory Labor Compensation (Protected floor)
    artisan_labor_wage = round(labor_hours * hourly_rate, 2)
    
    # 2. Base Production Cost
    base_production_cost = round(material_cost + artisan_labor_wage + overhead_cost + packaging_cost, 2)
    
    # 3. Sustainable Artisan Margin
    artisan_margin = round((base_production_cost * (desired_margin_pct / 100.0)), 2)
    
    # 4. Total Artisan Take-Home Payout (Labor Wage + Material + Overheads + Margin)
    artisan_net_payout = round(material_cost + artisan_labor_wage + overhead_cost + artisan_margin, 2)
    
    # 5. Ecosystem fees
    platform_fee = round((base_production_cost + artisan_margin) * 0.03, 2)  # Transparent 3% digital inclusion fee
    
    # 6. Fair Selling Price
    fair_selling_price = round(base_production_cost + artisan_margin + logistics_cost + platform_fee, 0)
    
    # Price tiers
    min_viable_price = round(base_production_cost + logistics_cost + platform_fee, 0)  # Break-even zero margin
    premium_boutique_price = round(fair_selling_price * 1.25, 0)
    
    # 7. Underpricing Defense Logic
    underpricing_warning = False
    warning_type = "NONE"
    advisory_message = ""
    
    if artisan_intended_price is not None and artisan_intended_price > 0:
        if artisan_intended_price < min_viable_price:
            underpricing_warning = True
            warning_type = "EXPLOITATION_RISK"
            shortfall = round(min_viable_price - artisan_intended_price, 2)
            advisory_message = (
                f"🚨 UNDERPRICING ALERT: Your proposed price of ₹{artisan_intended_price:,.0f} "
                f"falls below statutory production & logistics cost (₹{min_viable_price:,.0f}). "
                f"You will suffer an economic loss of ₹{shortfall:,.0f} and compromise your ₹{hourly_rate:.0f}/hr living wage!"
            )
        elif artisan_intended_price < fair_selling_price:
            warning_type = "MARGIN_ADVISORY"
            advisory_message = (
                f"ℹ️ Fair Value Guidance: We recommend ₹{fair_selling_price:,.0f} to protect your full "
                f"{desired_margin_pct:.0f}% artisan profit margin."
            )
        else:
            warning_type = "HEALTHY_MARGIN"
            advisory_message = "✅ Price covers statutory living wages and sustainable margin."
            
    return {
        "raw_material": material_cost,
        "labor_hours": labor_hours,
        "hourly_wage_rate": hourly_rate,
        "artisan_labor_wage": artisan_labor_wage,
        "overheads": overhead_cost,
        "packaging": packaging_cost,
        "logistics": logistics_cost,
        "platform_fee": platform_fee,
        "artisan_margin": artisan_margin,
        "base_production_cost": base_production_cost,
        "artisan_net_payout": artisan_net_payout,
        "fair_selling_price": fair_selling_price,
        "price_breakdown": [
            {"label": "Raw Material", "amount": material_cost, "icon": "🧶"},
            {"label": f"Artisan Labor ({labor_hours} hrs @ ₹{hourly_rate}/hr)", "amount": artisan_labor_wage, "icon": "⚖️"},
            {"label": "Overheads & Tools", "amount": overhead_cost, "icon": "⚙️"},
            {"label": "Packaging & Box", "amount": packaging_cost, "icon": "📦"},
            {"label": "Logistics & Delivery", "amount": logistics_cost, "icon": "🚚"},
            {"label": "Platform Digital Fee (3%)", "amount": platform_fee, "icon": "🌐"},
            {"label": f"Artisan Margin ({desired_margin_pct}%)", "amount": artisan_margin, "icon": "🌿"}
        ],
        "price_range": {
            "min_viable": min_viable_price,
            "recommended": fair_selling_price,
            "premium_boutique": premium_boutique_price
        },
        "wage_statutory_source": wage_info["statutory_reference"],
        "effective_date": wage_info["effective_date"],
        "underpricing_warning": underpricing_warning,
        "warning_type": warning_type,
        "advisory_message": advisory_message
    }