import os
import sys
import html
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_craft_svg(product_id, title, artisan, craft, state, category, color_theme, motif, gi_tag):
    bg_start, bg_end, accent_gold, border_color, text_color = color_theme
    
    # Escape for XML
    title_escaped = html.escape(str(title))
    artisan_escaped = html.escape(str(artisan))
    craft_escaped = html.escape(str(craft))
    state_escaped = html.escape(str(state))
    category_escaped = html.escape(str(category))
    motif_escaped = html.escape(str(motif))
    gi_tag_escaped = html.escape(str(gi_tag) if gi_tag else "HANDMADE AUTHENTIC")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 450" width="600" height="450">
  <defs>
    <linearGradient id="bgGrad_{product_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_start}" />
      <stop offset="100%" stop-color="{bg_end}" />
    </linearGradient>
    <linearGradient id="goldGrad_{product_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a" />
      <stop offset="50%" stop-color="{accent_gold}" />
      <stop offset="100%" stop-color="#b45309" />
    </linearGradient>
    <pattern id="weavePattern_{product_id}" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 0 10 L 20 10 M 10 0 L 10 20" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1.5"/>
    </pattern>
    <filter id="dropShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect width="600" height="450" fill="url(#bgGrad_{product_id})" />
  <rect width="600" height="450" fill="url(#weavePattern_{product_id})" />

  <!-- Outer Heritage Border -->
  <rect x="16" y="16" width="568" height="418" fill="none" stroke="{border_color}" stroke-width="3" rx="12" />
  <rect x="24" y="24" width="552" height="402" fill="none" stroke="url(#goldGrad_{product_id})" stroke-width="1" rx="8" stroke-dasharray="6,4" />

  <!-- Corner Traditional Accents -->
  <g fill="none" stroke="url(#goldGrad_{product_id})" stroke-width="2">
    <path d="M 28 48 L 48 48 L 48 28" />
    <path d="M 572 48 L 552 48 L 552 28" />
    <path d="M 28 402 L 48 402 L 48 422" />
    <path d="M 572 402 L 552 402 L 552 422" />
  </g>

  <!-- Center Decorative Craft Emblem -->
  <g transform="translate(300, 160)" filter="url(#dropShadow)">
    <circle r="75" fill="rgba(0,0,0,0.25)" stroke="url(#goldGrad_{product_id})" stroke-width="3" />
    <circle r="66" fill="none" stroke="{border_color}" stroke-width="1.5" stroke-dasharray="4,4" />
    
    <!-- Distinct Visual Centerpiece per Craft Category -->
    <text x="0" y="8" font-family="'Inter', sans-serif" font-size="42" text-anchor="middle" fill="#ffffff">
      {get_craft_icon(craft)}
    </text>
    <text x="0" y="32" font-family="'Inter', sans-serif" font-weight="700" font-size="11" text-anchor="middle" fill="{accent_gold}" letter-spacing="1">
      {motif_escaped.upper()}
    </text>
  </g>

  <!-- GI Certification Seal Badge -->
  <g transform="translate(480, 56)">
    <rect x="-60" y="-14" width="120" height="28" rx="14" fill="#047857" stroke="#34d399" stroke-width="1" />
    <text x="0" y="5" font-family="'Inter', sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">
      🛡️ {gi_tag_escaped}
    </text>
  </g>

  <!-- Category & Cluster Pill -->
  <g transform="translate(120, 56)">
    <rect x="-80" y="-14" width="160" height="28" rx="14" fill="rgba(0,0,0,0.35)" stroke="rgba(255,255,255,0.2)" stroke-width="1" />
    <text x="0" y="5" font-family="'Inter', sans-serif" font-size="11" font-weight="600" fill="#fef08a" text-anchor="middle">
      📍 {state_escaped} • {category_escaped}
    </text>
  </g>

  <!-- Product Details Card Bottom Banner -->
  <g transform="translate(30, 275)">
    <rect width="540" height="135" rx="10" fill="rgba(15, 23, 42, 0.75)" stroke="rgba(255, 255, 255, 0.15)" stroke-width="1" />
    
    <text x="20" y="32" font-family="'Playfair Display', Georgia, serif" font-weight="bold" font-size="19" fill="#ffffff">
      {title_escaped[:48] + ('...' if len(title_escaped) > 48 else '')}
    </text>
    
    <text x="20" y="58" font-family="'Inter', sans-serif" font-size="13" fill="#cbd5e1">
      Master Craftsman: <tspan font-weight="bold" fill="#fef08a">{artisan_escaped}</tspan> | {craft_escaped}
    </text>

    <!-- Living Wage & Authenticity Guarantee Badges -->
    <g transform="translate(20, 80)">
      <rect x="0" y="0" width="150" height="26" rx="4" fill="#0f766e" />
      <text x="75" y="17" font-family="'Inter', sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">
        ⚖️ Fair Living Wage
      </text>

      <rect x="160" y="0" width="150" height="26" rx="4" fill="#854d0e" />
      <text x="235" y="17" font-family="'Inter', sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">
        🧵 100% Handcrafted
      </text>

      <rect x="320" y="0" width="180" height="26" rx="4" fill="#1e3a8a" />
      <text x="410" y="17" font-family="'Inter', sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">
        🔒 Trust Escrow Protected
      </text>
    </g>
  </g>
</svg>"""
    return svg


def get_craft_icon(craft):
    c = craft.lower()
    if "paithani" in c or "saree" in c or "silk" in c:
        return "🥻"
    elif "madhubani" in c or "painting" in c or "folk" in c:
        return "🎨"
    elif "pottery" in c or "ceramic" in c or "blue" in c:
        return "🏺"
    elif "dhokra" in c or "metal" in c or "brass" in c:
        return "🗿"
    elif "bamboo" in c or "cane" in c:
        return "🎋"
    elif "kantha" in c or "embroidery" in c:
        return "🪡"
    elif "pashmina" in c or "cashmere" in c or "shawl" in c:
        return "🧣"
    return "🧵"


THEMES = {
    1: ("#4c0519", "#881337", "#facc15", "#e11d48", "#fff"), # Paithani Saree (Crimson Royal Zari)
    2: ("#451a03", "#78350f", "#fbbf24", "#d97706", "#fff"), # Madhubani (Ochre & Terracotta)
    3: ("#172554", "#1e3a8a", "#38bdf8", "#0284c7", "#fff"), # Blue Pottery (Cobalt Turquoise)
    4: ("#292524", "#44403c", "#f59e0b", "#d97706", "#fff"), # Dhokra Bell Metal (Antique Bronze)
    5: ("#022c22", "#064e3b", "#34d399", "#059669", "#fff"), # Kanchipuram (Emerald Temple Silk)
    6: ("#14532d", "#15803d", "#a3e635", "#65a30d", "#fff"), # Bamboo & Cane (Organic Forest)
    7: ("#311042", "#581c87", "#e879f9", "#a855f7", "#fff"), # Kantha Embroidery (Deep Royal Indigo)
    8: ("#0f172a", "#1e293b", "#cbd5e1", "#94a3b8", "#fff")  # Pashmina Cashmere (Himalayan Cloud)
}


def build_all_local_images():
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "images")
    os.makedirs(output_dir, exist_ok=True)
    
    from backend.seed_data import generate_full_products_catalog
    from datetime import datetime
    products = generate_full_products_catalog(datetime.utcnow().isoformat())
    
    for idx, p in enumerate(products, 1):
        artisan_id = p[0]
        artisan_name = p[1]
        title = p[2]
        category = p[6]
        craft = p[7]
        state = p[8]
        motifs = json.loads(p[11]) if isinstance(p[11], str) else p[11]
        motif_text = motifs[0] if motifs else "Authentic Weave"
        gi_number = p[24]
        
        theme = THEMES.get(artisan_id, THEMES[1])
        svg_content = generate_craft_svg(idx, title, artisan_name, craft, state, category, theme, motif_text, gi_number)
        
        filepath = os.path.join(output_dir, f"product_{idx}.svg")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
    print(f"Generated {len(products)} authentic local product SVG images in {output_dir}!")


if __name__ == "__main__":
    import json
    build_all_local_images()
