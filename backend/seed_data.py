"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - SEED DATA FOR SIH PROTOTYPE (80+ UNIQUE PRODUCTS)
==============================================================================
"""

import json
from datetime import datetime, timedelta
from backend.db import get_connection

GOOGLE_IMAGE_LINKS = {
    1: "/static/images/product_1.jpg",
    2: "/static/images/product_2.jpg",
    3: "/static/images/product_3.jpg",
    4: "/static/images/product_4.jpg",
    5: "/static/images/product_5.jpg",
    6: "/static/images/product_6.jpg",
    7: "/static/images/product_7.jpg",
    8: "/static/images/product_8.jpg",
    9: "/static/images/product_9.jpg",
    10: "/static/images/product_10.jpg",
    11: "/static/images/product_11.jpg",
    12: "/static/images/product_12.jpg",
    13: "/static/images/product_13.jpg",
    14: "/static/images/product_14.jpg",
    15: "https://indianfolkart.org/wp-content/uploads/2021/08/Madhubani-Anjali-09.jpg",
    16: "/static/images/product_16.jpg",
    17: "/static/images/product_17.jpg",
    18: "/static/images/product_18.jpg",
    19: "/static/images/product_19.jpg",
    20: "/static/images/product_20.jpg",
    21: "/static/images/product_21.jpg",
    22: "https://cdn.vibecity.in/providers/61dc119f7864df0011da13c3/13ed9ac8-4a74-4e8f-8966-e0baff65939c_dc64f2b2-d9e1-4eed-a676-b91ebe77e32c.png",
    23: "https://www.neerjainternational.com/sites/default/files/NBPWP-8011-FRONT.jpg",
    24: "/static/images/product_24.jpg",
    25: "/static/images/product_25.jpg",
    26: "/static/images/product_26.jpg",
    27: "/static/images/product_27.jpg",
    28: "/static/images/product_28.jpg",
    29: "/static/images/product_29.jpg",
    30: "/static/images/product_30.jpg",
    31: "/static/images/product_31.jpg",
    32: "/static/images/product_32.jpg",
    33: "/static/images/product_33.jpg",
    34: "/static/images/product_34.jpg",
    35: "https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-4lcndh.jpg",
    36: "https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-dbxk1m.jpg",
    37: "https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-yopuoa.jpg",
    38: "https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-ln3f4c.jpg",
    39: "https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-4lcndh.jpg",
    40: "/static/images/product_40.jpg",
    41: "/static/images/product_41.jpg",
    42: "/static/images/product_42.jpg",
    43: "/static/images/product_43.jpg",
    44: "/static/images/product_44.jpg",
    45: "/static/images/product_45.jpg",
    46: "/static/images/product_46.jpg",
    47: "/static/images/product_47.jpg",
    48: "/static/images/product_48.jpg",
    49: "/static/images/product_49.jpg",
    50: "/static/images/product_50.jpg",
    51: "/static/images/product_51.jpg",
    52: "/static/images/product_52.jpg",
    53: "/static/images/product_53.jpg",
    54: "/static/images/product_54.jpg",
    55: "/static/images/product_55.jpg",
    56: "/static/images/product_56.jpg",
    57: "/static/images/product_57.jpg",
    58: "/static/images/product_58.jpg",
    59: "/static/images/product_59.jpg",
    60: "/static/images/product_60.jpg",
    61: "/static/images/product_61.jpg",
    62: "/static/images/product_62.jpg",
    63: "/static/images/product_63.jpg",
    64: "/static/images/product_64.jpg",
    65: "/static/images/product_65.jpg",
    66: "/static/images/product_66.jpg",
    67: "/static/images/product_67.jpg",
    68: "/static/images/product_68.jpg",
    69: "/static/images/product_69.jpg",
    70: "/static/images/product_70.jpg",
    71: "/static/images/product_71.jpg",
    72: "/static/images/product_72.jpg",
    73: "/static/images/product_73.jpg",
    74: "/static/images/product_74.jpg",
    75: "/static/images/product_75.jpg",
    76: "https://cdn.vibecity.in/providers/61dc119f7864df0011da13c3/13ed9ac8-4a74-4e8f-8966-e0baff65939c_dc64f2b2-d9e1-4eed-a676-b91ebe77e32c.png",
    77: "https://www.neerjainternational.com/sites/default/files/NBPWP-8011-FRONT.jpg",
    78: "/static/images/product_78.jpg",
    79: "/static/images/product_79.jpg",
    80: "/static/images/product_80.jpg"
}

def generate_full_products_catalog(now: str):
    products = []
    
    # 1. Rishikant Mishra (Maharashtra - Paithani Silk) - 10 Products with unique handloom silk imagery
    p1 = [
        ("Authentic Handwoven Paithani Silk Saree", "Pure Mulberry Silk saree with hand-woven golden zari peacock pallu motif.",
         "Handcrafted in the historic Yeola cluster using centuries-old interlocking weft techniques.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["Pure Mulberry Silk", "Tested Golden Zari", "Natural Dyes"], "Interlocking Weft Pitloom", ["Mor (Peacock)", "Muniyā", "Asawali"],
         "6.3 meters with blouse", "780g", "Dry clean only, wrap in soft cotton cloth",
         ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
         800.0, 15.0, 65.0, 2344.0, 2344.0, 4, "GI-MH-001"),

        ("Royal Bridal Kadial Paithani Saree", "Double-interlocked solid contrast border Kadial Paithani in crimson red and emerald zari.",
         "A masterpiece taking 28 days of dual-artisan synchronization on the pitloom.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["Pure Mulberry Silk", "Heavy Zari Weft", "Natural Lac Dye"], "Kadial Double Weft Technique", ["Lotus Petals", "Royal Peacock", "Kalka"],
         "6.3 meters with blouse", "890g", "Dry clean only in muslin wrap",
         ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
         1500.0, 28.0, 65.0, 4250.0, 4250.0, 2, "GI-MH-001"),

        ("Yeola Asawali Floral Motif Paithani Saree", "Delicate flower pot (Asawali) vine motifs woven seamlessly along golden zari borders.",
         "Generational craft heritage preserving 18th-century Peshwa court aesthetics.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["Mulberry Silk", "Silver Gold Zari"], "Interlocking Weft", ["Asawali (Vines)", "Flower Pots"],
         "6.3 meters", "750g", "Dry clean only",
         ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
         950.0, 18.0, 65.0, 2850.0, 2850.0, 3, "GI-MH-001"),

        ("Traditional Muniyā Border Paithani Saree", "Parrot motif (Muniyā) geometric border in vibrant bottle green with golden pallu.",
         "Hand-interlocked weft structure with authentic Yeola guild certification.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["Pure Silk", "Golden Zari"], "Pitloom Weave", ["Muniyā (Parrots)", "Coin Butti"],
         "6.3 meters", "760g", "Dry clean only",
         ["https://images.unsplash.com/photo-1610030469668-9655ecdd9745?w=700&auto=format&fit=crop&q=80"],
         900.0, 16.0, 65.0, 2650.0, 2650.0, 3, "GI-MH-001"),

        ("Tissue Silk Pure Gold Zari Paithani Saree", "Ultra-fine tissue silk with full zari brocade weaving for royal festivities.",
         "Woven with 100% fine tested metallic thread over organic warp.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["Tissue Silk", "Gold Zari Brocade"], "Fine Tissue Weft", ["Sun Radiance", "Mor Butta"],
         "6.3 meters", "820g", "Dry clean only",
         ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
         1600.0, 30.0, 65.0, 4600.0, 4600.0, 2, "GI-MH-001"),

        ("Paithani Silk Handwoven Dupatta", "Luxurious festive dupatta featuring grand peacock roundels on shimmering pure silk.",
         "Perfect festive accessory handcrafted in rural Maharashtra cluster.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["Pure Silk", "Zari Motifs"], "Pitloom Interlocking", ["Peacock Roundels", "Zari Stripes"],
         "2.5 meters x 36 inches", "320g", "Dry clean only",
         ["https://images.unsplash.com/photo-1583391733975-0010c2c2f829?w=700&auto=format&fit=crop&q=80"],
         450.0, 9.0, 65.0, 1450.0, 1450.0, 6, "GI-MH-001"),

        ("Narali Border Festive Silk Paithani", "Coconut-grove (Narali) serrated border design symbolizing prosperity.",
         "Woven with traditional shuttle movements by master artisan Rishikant Mishra.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["Mulberry Silk", "Zari"], "Interlocking Pitloom", ["Narali Border", "Star Butti"],
         "6.3 meters", "740g", "Dry clean only",
         ["https://images.unsplash.com/photo-1617627143714-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
         850.0, 14.0, 65.0, 2450.0, 2450.0, 4, "GI-MH-001"),

        ("Brocade Pallu Paithani Handloom Saree", "Heavy zari brocade dense pallu with 7 distinct peacock motifs.",
         "Requires 120 hours of meticulous handloom craftsmanship.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["Pure Silk", "Heavy Zari"], "Dense Brocade Weave", ["Royal Peacocks", "Lotus Blooms"],
         "6.3 meters", "910g", "Dry clean only",
         ["https://images.unsplash.com/photo-1610030469850-9655ecdd9745?w=700&auto=format&fit=crop&q=80"],
         1800.0, 32.0, 65.0, 5100.0, 5100.0, 1, "GI-MH-001"),

        ("Pastel Peach Contemporary Paithani Saree", "Modern pastel peach body adorned with classic heritage zari motifs.",
         "Fusion of urban elegance and generational rural handloom skill.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["Organza Silk Blend", "Fine Gold Zari"], "Fine Warp Weave", ["Subtle Mor", "Floral Buds"],
         "6.3 meters", "680g", "Dry clean only",
         ["https://images.unsplash.com/photo-1609357605199-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
         750.0, 13.0, 65.0, 2150.0, 2150.0, 5, "GI-MH-001"),

        ("Heritage Vintage Kalanjali Paithani Saree", "Collector edition saree reviving 19th-century royal court weaves.",
         "Limited artisanal creation with certified living wage escrow protection.", "Handloom & Silk", "Paithani Silk", "Maharashtra",
         ["100% Pure Silk", "Vintage Gold Thread"], "Traditional Interlocking", ["Kalanjali Pot", "Peshwa Borders"],
         "6.3 meters", "840g", "Dry clean only",
         ["https://images.unsplash.com/photo-1583391733980-0010c2c2f829?w=700&auto=format&fit=crop&q=80"],
         1400.0, 25.0, 65.0, 3950.0, 3950.0, 2, "GI-MH-001")
    ]
    for p in p1:
        prod_idx = len(products) + 1
        img_url = GOOGLE_IMAGE_LINKS.get(prod_idx, f"https://encrypted-tbn0.gstatic.com/images?q=tbn:product_{prod_idx}")
        products.append((1, "Rishikant Mishra", p[0], p[1], p[2], p[2], p[3], p[4], p[5], json.dumps(p[6]), p[7], json.dumps(p[8]), p[9], p[10], p[11], json.dumps([img_url]), p[13], p[14], p[15], p[16], p[16], p[17], 0, 4, p[18], 1, json.dumps(["GI-Protected", "Pure Silk", "Fair Wage"]), "PUBLISHED", 80, now, now))

    # 2. Meenakshi Jha (Bihar - Madhubani Art) - 10 Products with unique folk canvas painting imagery
    p2 = [
        ("Traditional Madhubani Mithila Tree of Life Painting", "Intricately painted folk artwork using handmade paper and natural vegetable extracts.",
         "Depicts the mythical Tree of Life surrounded by auspicious fish and bird motifs.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Handmade Paper", "Organic Dyes"], "Fine Line Nib Drawing", ["Tree of Life", "Matsya"], "22 x 30 in", "320g", "Keep dry",
         ["https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=700&auto=format&fit=crop&q=80"],
         350.0, 8.0, 62.0, 1220.0, 1220.0, 5, "GI-BR-002"),

        ("Madhubani Kohbar Bridal Blessings Artwork", "Sacred matrimonial folk painting with lotus and bamboo cosmic symbols.",
         "Painted by master artist Meenakshi Jha using traditional bamboo sticks.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Handmade Cloth Canvas", "Natural Pigments"], "Bharni Painting", ["Kohbar", "Lotus", "Sun"], "24 x 36 in", "380g", "Frame behind glass",
         ["https://images.unsplash.com/photo-1577083552431-6e5fd01aa342?w=700&auto=format&fit=crop&q=80"],
         450.0, 12.0, 62.0, 1650.0, 1650.0, 3, "GI-BR-002"),

        ("Matsya Avatar Fish Folk Painting", "Dual sacred fish swimming in cosmic lotus pond symbolizing prosperity.",
         "Natural vegetable extracts of marigold and turmeric on acid-free paper.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Handmade Rag Paper", "Turmeric & Indigo"], "Kachni Line Work", ["Matsya", "Waves", "Water Lilies"], "18 x 24 in", "250g", "Keep dry",
         ["https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=700&auto=format&fit=crop&q=80"],
         280.0, 6.0, 62.0, 950.0, 950.0, 6, "GI-BR-002"),

        ("Sun God Surya Mandala Painting", "Auspicious solar deity radiating sacred Mithila geometric mandalas.",
         "Symbol of vitality and positive energy for living room wall decor.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Handmade Paper", "Soot & Ochre"], "Fine Line Geometry", ["Surya", "Mandala Rays", "Flora"], "20 x 20 in", "290g", "Dust with dry cloth",
         ["https://images.unsplash.com/photo-1577083552792-a0d461cb1dd6?w=700&auto=format&fit=crop&q=80"],
         300.0, 7.0, 62.0, 1050.0, 1050.0, 4, "GI-BR-002"),

        ("Radha Krishna in Vrindavan Madhubani Canvas", "Romantic divine folk depiction under blooming Kadamba tree.",
         "Intricate village scene framed with traditional double-bordered floral vines.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Cotton Canvas", "Natural Herbal Dyes"], "Color Fill Bharni", ["Radha Krishna", "Peacock", "Kadamba Tree"], "30 x 40 in", "520g", "Dust gently",
         ["https://images.unsplash.com/photo-1582561424760-0321d75e81fa?w=700&auto=format&fit=crop&q=80"],
         600.0, 16.0, 62.0, 2100.0, 2100.0, 2, "GI-BR-002"),

        ("Royal Elephant Procession Mithila Folk Art", "Ceremonial elephant carrying royal palanquin amidst village celebration.",
         "Hand-painted with bamboo stylus using charcoal black and terracotta red.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Handmade Paper", "Charcoal & Plant Dyes"], "Kachni Line Drawing", ["Gaja (Elephant)", "Dancers", "Lotus"], "16 x 20 in", "220g", "Keep dry",
         ["https://images.unsplash.com/photo-1579783901467-31b607736a1b?w=700&auto=format&fit=crop&q=80"],
         250.0, 5.0, 62.0, 850.0, 850.0, 5, "GI-BR-002"),

        ("Ganga River Goddess Folk Tapestry", "Sacred river goddess descending with celestial makara crocodile.",
         "Authentic GI-certified Mithila spiritual artwork.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Handmade Silk Paper", "Indigo & Beetroot Dyes"], "Fine Line Freehand", ["Ganga Devi", "Makara", "Sacred Pot"], "22 x 28 in", "310g", "Framed",
         ["https://images.unsplash.com/photo-1577083553258-8686d1a4e156?w=700&auto=format&fit=crop&q=80"],
         380.0, 9.0, 62.0, 1350.0, 1350.0, 3, "GI-BR-002"),

        ("Peacock & Peahen Harmony Folk Art", "Auspicious bird couple perched on pomegranate branches.",
         "Painted by master artist Meenakshi Jha in Jitwarpur craft village.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Organic Rag Paper", "Natural Forest Pigments"], "Fine Kachni Strokes", ["Peacock Pair", "Floral Buds"], "15 x 22 in", "240g", "Dust with cloth",
         ["https://images.unsplash.com/photo-1582561424557-4f676060c5a2?w=700&auto=format&fit=crop&q=80"],
         270.0, 6.0, 62.0, 920.0, 920.0, 7, "GI-BR-002"),

        ("Village Harvest Festival Madhubani Painting", "Rural women carrying golden grain sheaves during Chhath festival.",
         "Celebration of agricultural abundance and cosmic balance.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Handmade Paper", "Yellow Ochre & Soot"], "Bharni Folk Style", ["Harvest Women", "Grain Baskets", "Sun"], "20 x 30 in", "340g", "Frame behind glass",
         ["https://images.unsplash.com/photo-1579783926514-a3fb3927b675?w=700&auto=format&fit=crop&q=80"],
         390.0, 10.0, 62.0, 1420.0, 1420.0, 4, "GI-BR-002"),

        ("Mithila Floral Mandala Meditation Painting", "Complex 64-petal lotus mandala drawn with single-hair fine brush strokes.",
         "Ideal spiritual meditation artwork for calm living spaces.", "Folk Art & Decor", "Madhubani Painting", "Bihar",
         ["Handmade Cloth Paper", "Natural Clay & Mineral Dyes"], "Geometric Kachni", ["64-Petal Lotus", "Concentric Rings"], "24 x 24 in", "360g", "Keep dry",
         ["https://images.unsplash.com/photo-1577083552480-6e5fd01aa342?w=700&auto=format&fit=crop&q=80"],
         420.0, 11.0, 62.0, 1550.0, 1550.0, 3, "GI-BR-002")
    ]
    for p in p2:
        prod_idx = len(products) + 1
        img_url = GOOGLE_IMAGE_LINKS.get(prod_idx, f"https://encrypted-tbn0.gstatic.com/images?q=tbn:product_{prod_idx}")
        products.append((2, "Meenakshi Jha", p[0], p[1], p[2], p[2], p[3], p[4], p[5], json.dumps(p[6]), p[7], json.dumps(p[8]), p[9], p[10], p[11], json.dumps([img_url]), p[13], p[14], p[15], p[16], p[16], p[17], 0, 3, p[18], 1, json.dumps(["GI-Protected", "Folk Art", "Natural Dyes"]), "PUBLISHED", 65, now, now))

    # 3. Devendra Sharma (Rajasthan - Blue Pottery) - 10 Products with unique ceramic/pottery imagery
    p3 = [
        ("Handcrafted Jaipur Blue Pottery Floral Motif Vase", "Lead-free glazed decorative vase crafted with quartz stone powder (no clay).",
         "Fired with turquoise copper oxide and cobalt blue mineral glaze.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Ground Quartz", "Cullet Glass", "Cobalt Glaze"], "Low Heat Kiln Glaze", ["Persian Arabesque", "Petals"], "10 in (H) x 5 in (Dia)", "650g", "Wipe damp sponge",
         ["https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=700&auto=format&fit=crop&q=80"],
         200.0, 5.0, 65.0, 815.0, 815.0, 8, "GI-RJ-003"),

        ("Jaipur Blue Pottery Decorative Wall Plate", "Ornate floral arabesque wall plate with vibrant Persian cobalt blue glaze.",
         "Crafted without clay using quartz stone composite and copper oxide.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Quartz Stone", "Mineral Glaze"], "Hand-Molded Firing", ["Persian Floral", "Geometric Border"], "12 in (Dia)", "720g", "Wall hook attached",
         ["https://images.unsplash.com/photo-1615865417491-9941019fbc00?w=700&auto=format&fit=crop&q=80"],
         250.0, 6.0, 65.0, 950.0, 950.0, 6, "GI-RJ-003"),

        ("Handmade Blue Pottery Ceramic Tea Mug Set (Set of 2)", "Artisanal glazed tea mugs featuring hand-painted floral blooms.",
         "Lead-free non-toxic glaze safe for hot beverages.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Quartz Powder", "Food-grade Glaze"], "Kiln Glazed", ["Floral Vines", "Turquoise Ring"], "350ml each", "580g", "Gentle hand wash",
         ["https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=700&auto=format&fit=crop&q=80"],
         180.0, 4.0, 65.0, 680.0, 680.0, 10, "GI-RJ-003"),

        ("Blue Pottery Tabletop Indoor Succulent Planter", "Decorative hexagonal planter with drainage hole in traditional Jaipur motifs.",
         "Hand-crafted by master artisan Devendra Sharma.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Quartz Ceramic", "Natural Multani Mitti"], "Hand-Molded", ["Hexagonal Lattice", "Petal Sprays"], "6 in (H) x 6 in (W)", "620g", "Indoor plant safe",
         ["https://images.unsplash.com/photo-1578749556500-bc2c40e68b61?w=700&auto=format&fit=crop&q=80"],
         190.0, 4.5, 65.0, 720.0, 720.0, 7, "GI-RJ-003"),

        ("Royal Indigo Blue Pottery Serving Bowl", "Deep serving bowl with dual-tone Persian turquoise and cobalt blue motifs.",
         "Stunning centerpiece for royal dining and table decor.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Quartz Composite", "Cobalt Oxide"], "Glaze Fired", ["Persian Vines", "Border Waves"], "9 in (Dia) x 4 in (H)", "850g", "Hand wash only",
         ["https://images.unsplash.com/photo-1615865417450-9941019fbc00?w=700&auto=format&fit=crop&q=80"],
         280.0, 6.0, 65.0, 1020.0, 1020.0, 5, "GI-RJ-003"),

        ("Blue Pottery Coaster Set with Wooden Stand (Set of 4)", "Square ceramic drink coasters hand-painted in traditional Rajasthani motifs.",
         "Includes sheesham wood holder.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Quartz Pottery", "Sheesham Wood"], "Hand-Painted Glaze", ["Floral Arabesque", "Border Lines"], "4 x 4 in each", "480g", "Wipe clean",
         ["https://images.unsplash.com/photo-1514432324620-a09d9b4aefdd?w=700&auto=format&fit=crop&q=80"],
         160.0, 3.5, 65.0, 580.0, 580.0, 12, "GI-RJ-003"),

        ("Persian Royal Urn with Lid", "Classic lidded decorative urn with hand-painted Persian floral symmetry.",
         "Fired in traditional low-temperature kilns in Jaipur cluster.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Quartz Stone", "Copper Oxide"], "Wheel & Molded", ["Persian Leaf", "Dome Lid Ring"], "12 in (H) x 7 in (Dia)", "1100g", "Handle with care",
         ["https://images.unsplash.com/photo-1578749556588-bc2c40e68b61?w=700&auto=format&fit=crop&q=80"],
         380.0, 8.0, 65.0, 1380.0, 1380.0, 3, "GI-RJ-003"),

        ("Blue Pottery Ceramic Wall Clock", "Functional wall timepiece featuring hand-painted sunburst ceramic dial.",
         "Fitted with silent quartz battery movement.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Quartz Ceramic", "Quartz Movement"], "Hand-Molded Dial", ["Sunburst Rays", "Arabic Numerals"], "10 in (Dia)", "740g", "Wall mountable",
         ["https://images.unsplash.com/photo-1615865417550-9941019fbc00?w=700&auto=format&fit=crop&q=80"],
         320.0, 7.0, 65.0, 1180.0, 1180.0, 4, "GI-RJ-003"),

        ("Decorative Handcrafted Ceramic Door Knobs (Set of 4)", "Vintage style cabinet and wardrobe drawer pull handles.",
         "Includes brass screws and washers for easy DIY installation.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Glazed Quartz", "Solid Brass Fittings"], "Molded Glaze", ["Floral Petals", "Indigo Ring"], "1.5 in (Dia) each", "280g", "Easy screw install",
         ["https://images.unsplash.com/photo-1514432324640-a09d9b4aefdd?w=700&auto=format&fit=crop&q=80"],
         140.0, 3.0, 65.0, 490.0, 490.0, 15, "GI-RJ-003"),

        ("Jaipur Royal Ceramic Tea Pot", "Exquisite ceremonial teapot with curved spout and thermal-insulated ceramic lid.",
         "Preserving 14th-century craft heritage introduced by Jaipur Maharajas.", "Ceramics & Decor", "Blue Pottery", "Rajasthan",
         ["Quartz Stone Composite", "Lead-free Glaze"], "Hand-Glazed Firing", ["Persian Arabesque", "Cobalt Trim"], "750ml", "690g", "Hand wash gently",
         ["https://images.unsplash.com/photo-1578749556550-bc2c40e68b61?w=700&auto=format&fit=crop&q=80"],
         310.0, 6.5, 65.0, 1120.0, 1120.0, 4, "GI-RJ-003")
    ]
    for p in p3:
        prod_idx = len(products) + 1
        img_url = GOOGLE_IMAGE_LINKS.get(prod_idx, f"https://encrypted-tbn0.gstatic.com/images?q=tbn:product_{prod_idx}")
        products.append((3, "Devendra Sharma", p[0], p[1], p[2], p[2], p[3], p[4], p[5], json.dumps(p[6]), p[7], json.dumps(p[8]), p[9], p[10], p[11], json.dumps([img_url]), p[13], p[14], p[15], p[16], p[16], p[17], 0, 3, p[18], 1, json.dumps(["GI-Protected", "Ceramics", "No-Clay Pottery"]), "PUBLISHED", 55, now, now))

    # 4. Gurucharan Mohapatra (Odisha - Dhokra Metallurgy) - 10 Products with unique brass/bronze sculpture imagery
    p4 = [
        ("Tribal Dhokra Lost-Wax Bell Metal Dancing Figurine", "4,000-year prehistoric lost-wax cast brass figurine of a tribal folk dancer.",
         "Cast in Bastar/Mayurbhanj cluster using beeswax wires over clay core.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["Recycled Bell Metal", "Brass Alloy", "Natural Beeswax"], "Lost-Wax (Cire Perdue)", ["Tribal Dancer", "Spirals"], "9.5 x 3.5 in", "920g", "Clean with dry brass cloth",
         ["https://images.unsplash.com/photo-1567825836480-4c379a5840ca?w=700&auto=format&fit=crop&q=80"],
         600.0, 18.0, 60.0, 2425.0, 2425.0, 2, "GI-OD-004"),

        ("Bastar Royal War Elephant Dhokra Sculpture", "Solid cast bell-metal royal war elephant with traditional howdah canopy and rider.",
         "Hand-sculpted wax lattice by master metallurgist Gurucharan Mohapatra.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["Brass & Bell Metal", "River Clay Core"], "Lost-Wax Casting", ["Gaja (Elephant)", "Lattice Howdah"], "8 x 7 in", "1250g", "Brass polish sparingly",
         ["https://images.unsplash.com/photo-1544816155-12df9643f363?w=700&auto=format&fit=crop&q=80"],
         750.0, 22.0, 60.0, 2950.0, 2950.0, 2, "GI-OD-004"),

        ("Sacred Nandi Bull Dhokra Figurine", "Auspicious tribal humped Nandi bull adorned with cast bell-metal garlands.",
         "Harappan metallurgical tradition preserved across thousands of years.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["Bell Metal Brass", "Beeswax Mold"], "Pit Furnace Casting", ["Humped Bull", "Necklace Beads"], "6 x 6 in", "780g", "Dust with soft cloth",
         ["https://images.unsplash.com/photo-1567825836450-4c379a5840ca?w=700&auto=format&fit=crop&q=80"],
         480.0, 14.0, 60.0, 1850.0, 1850.0, 3, "GI-OD-004"),

        ("Tribal Folk Musicians Ensemble (Set of 3)", "Trio of tribal musicians playing dhol drum, flute, and traditional horn.",
         "Handcrafted lost-wax brass figures celebrating forest folk festivities.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["Brass Alloy", "Natural Beeswax"], "Cire Perdue Casting", ["Dhol Drummer", "Flute Player", "Horn Blower"], "7 in (H) each", "1100g", "Dry cloth wipe",
         ["https://images.unsplash.com/photo-1544816155-12df9643f350?w=700&auto=format&fit=crop&q=80"],
         650.0, 20.0, 60.0, 2600.0, 2600.0, 2, "GI-OD-004"),

        ("Dhokra Forest Deer Family Pair", "Pair of graceful forest deer with ribbed spiral antlers and wirework body.",
         "Symbol of forest ecology and tribal harmony with nature.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["Bell Metal Brass"], "Lost-Wax Single Mold", ["Spiral Antlers", "Wire Lattice"], "8 in (H) and 6 in (H)", "890g", "Wipe clean",
         ["https://images.unsplash.com/photo-1567825836470-4c379a5840ca?w=700&auto=format&fit=crop&q=80"],
         520.0, 15.0, 60.0, 2050.0, 2050.0, 3, "GI-OD-004"),

        ("Tribal Horse Rider Warrior Figurine", "Heroic tribal chieftain mounted on an elongated ceremonial horse.",
         "Sculpted using beeswax wires and pit-cast in Bastar.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["Brass Alloy", "Beeswax"], "Lost-Wax Metallurgy", ["Horse Rider", "Spear", "Shield"], "10 x 5 in", "1050g", "Clean with dry cloth",
         ["https://images.unsplash.com/photo-1544816155-12df9643f370?w=700&auto=format&fit=crop&q=80"],
         580.0, 17.0, 60.0, 2250.0, 2250.0, 2, "GI-OD-004"),

        ("Dhokra Traditional Oil Diya Lamp", "Decorative oil diya lamp with peacock handle and five wick spouts.",
         "Cast in heavy bell-metal brass for auspicious home pooja lighting.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["Heavy Bell Metal"], "Furnace Pit Cast", ["Peacock Handle", "5-Wick Diya"], "8 in (H) x 5 in (W)", "720g", "Washable with pitambari",
         ["https://images.unsplash.com/photo-1567825836460-4c379a5840ca?w=700&auto=format&fit=crop&q=80"],
         380.0, 10.0, 60.0, 1450.0, 1450.0, 5, "GI-OD-004"),

        ("Tribal Goddess Wall Hanging Mask", "Expressive tribal spirit face mask with sunburst crown and circular earrings.",
         "Protective wall talisman handcrafted with ancient lost-wax technique.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["Brass & Bronze Alloy"], "Lost-Wax Wall Relief", ["Sun Crown", "Spiral Earrings"], "9 x 6 in", "640g", "Wall hook ready",
         ["https://images.unsplash.com/photo-1544816155-12df9643f380?w=700&auto=format&fit=crop&q=80"],
         390.0, 11.0, 60.0, 1520.0, 1520.0, 4, "GI-OD-004"),

        ("Auspicious Dhokra Wise Owl Figurine", "Detailed wise owl with concentric eye wirework and ribbed feathers.",
         "Associated with goddess Lakshmi and knowledge in Indian tradition.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["Solid Bell Metal"], "Lost-Wax Single Cast", ["Concentric Eyes", "Wing Feathers"], "5.5 x 4 in", "580g", "Dust with cloth",
         ["https://images.unsplash.com/photo-1567825836490-4c379a5840ca?w=700&auto=format&fit=crop&q=80"],
         340.0, 9.0, 60.0, 1280.0, 1280.0, 6, "GI-OD-004"),

        ("Ceremonial Tribal Hanging Wind Bell", "Sonorous cast bronze temple bell with elephant finial and tuned chime.",
         "Produces clear resonant acoustic tone when rung.", "Metallurgy & Sculpture", "Dhokra Bell Metal", "Odisha",
         ["High-Tin Bronze & Brass"], "Acoustic Bell Casting", ["Elephant Finial", "Tuned Clapper"], "7 in (H) x 4 in (Dia)", "810g", "Hang indoors/porch",
         ["https://images.unsplash.com/photo-1544816155-12df9643f390?w=700&auto=format&fit=crop&q=80"],
         420.0, 12.0, 60.0, 1620.0, 1620.0, 4, "GI-OD-004")
    ]
    for p in p4:
        prod_idx = len(products) + 1
        img_url = GOOGLE_IMAGE_LINKS.get(prod_idx, f"https://encrypted-tbn0.gstatic.com/images?q=tbn:product_{prod_idx}")
        products.append((4, "Gurucharan Mohapatra", p[0], p[1], p[2], p[2], p[3], p[4], p[5], json.dumps(p[6]), p[7], json.dumps(p[8]), p[9], p[10], p[11], json.dumps([img_url]), p[13], p[14], p[15], p[16], p[16], p[17], 0, 4, p[18], 1, json.dumps(["GI-Protected", "Lost-Wax", "Tribal Metallurgy"]), "PUBLISHED", 70, now, now))

    # 5. Kalyanasundaram Swamy (Tamil Nadu - Kanchipuram Silk) - 10 Products with unique South Indian silk saree imagery
    p5 = [
        ("Pure Zari Handwoven Kanchipuram Temple Border Silk Saree", "Solid crimson body with authentic emerald Korvai temple border and silver electroplated golden zari.",
         "Interlocked with 3-shuttle technique by master weaver Kalyanasundaram Swamy in Kanchipuram.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["Pure Mulberry Silk", "Silver Golden Zari"], "Three-Shuttle Korvai", ["Temple Gopuram", "Rudraksha", "Mayil"], "6.2 meters", "850g", "Dry clean only",
         ["https://images.unsplash.com/photo-1610030469668-9655ecdd9745?w=700&auto=format&fit=crop&q=80"],
         1200.0, 22.0, 68.0, 3850.0, 3850.0, 2, "GI-TN-005"),

        ("Royal Peacock Teal Bridal Kanchipuram Silk Saree", "Opulent peacock teal with contrast magenta border and dense pure gold zari brocade.",
         "Masterpiece handwoven over 3 weeks of rhythmic pitloom action.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["100% Mulberry Silk", "Heavy Zari"], "Solid Korvai Interlock", ["Peacock (Mayil)", "Mango Butta"], "6.2 meters", "920g", "Dry clean only",
         ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
         1400.0, 26.0, 68.0, 4450.0, 4450.0, 2, "GI-TN-005"),

        ("Muhurtham Gold Brocade Kanchipuram Silk Saree", "Gleaming pure gold tissue body designed for South Indian bridal wedding ceremonies.",
         "Heavy weight pure silk certified with Silk Mark and GI provenance.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["Pure Silk Warp", "Tested Zari Brocade"], "Full Tissue Weft", ["Floral Jaal", "Gopuram Base"], "6.2 meters", "980g", "Dry clean only",
         ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
         1650.0, 30.0, 68.0, 5200.0, 5200.0, 1, "GI-TN-005"),

        ("Emerald Green & Ruby Red Korvai Silk Saree", "Traditional auspicious color combination with solid interlocking temple towers.",
         "Woven by master artisan Kalyanasundaram Swamy in Kanchipuram cluster.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["Mulberry Silk", "Gold Zari"], "Korvai Pitloom", ["Temple Spikes", "Coin Butti"], "6.2 meters", "840g", "Dry clean only",
         ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
         1100.0, 20.0, 68.0, 3500.0, 3500.0, 3, "GI-TN-005"),

        ("Aubergine Purple Gold Zari Kanchipuram Saree", "Rich deep purple body sprinkled with silver zari floral medallions.",
         "Commanding royal drape woven with 3-ply twisted silk yarn.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["3-Ply Silk", "Silver Gold Zari"], "Interlocking Border", ["Floral Medallions", "Chevron Trim"], "6.2 meters", "860g", "Dry clean only",
         ["https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=700&auto=format&fit=crop&q=80"],
         1150.0, 21.0, 68.0, 3650.0, 3650.0, 3, "GI-TN-005"),

        ("Mango Paisley Motif Kanchipuram Silk Saree", "Classic golden mango paisley motifs woven across vibrant sunrise orange body.",
         "Protected living wage payout secured in trust escrow.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["Pure Mulberry Silk", "Zari"], "Pitloom Weaving", ["Manga (Mango)", "Rudraksha Band"], "6.2 meters", "830g", "Dry clean only",
         ["https://images.unsplash.com/photo-1583391733975-0010c2c2f829?w=700&auto=format&fit=crop&q=80"],
         1050.0, 19.0, 68.0, 3350.0, 3350.0, 4, "GI-TN-005"),

        ("Mustard Yellow Festive Kanchipuram Saree", "Bright mustard yellow with maroon contrast pallu and elephant roundels.",
         "Handcrafted by generational weavers in Tamil Nadu.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["Pure Silk", "Gold Thread"], "Korvai Border", ["Yali (Mythical Beast)", "Elephant"], "6.2 meters", "810g", "Dry clean only",
         ["https://images.unsplash.com/photo-1617627143714-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
         980.0, 18.0, 68.0, 3150.0, 3150.0, 3, "GI-TN-005"),

        ("Kanchipuram Pure Silk Handwoven Stole", "Festive luxury unisex stole with intricate Korvai zari border bands.",
         "Compact luxury accessory for weddings and traditional functions.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["Mulberry Silk", "Tested Zari"], "Fine Shuttle Weave", ["Gopuram Temple", "Zari Stripes"], "2.2 meters x 30 in", "310g", "Dry clean only",
         ["https://images.unsplash.com/photo-1609357605199-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
         480.0, 8.0, 68.0, 1480.0, 1480.0, 5, "GI-TN-005"),

        ("Soft Silk Pastel Mint Kanchipuram Saree", "Lightweight soft silk weave with delicate silver zari borders for modern occasions.",
         "Drapes effortlessly with smooth butter-soft pure silk feel.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["Soft Mulberry Silk", "Silver Zari"], "Lightweight Weft", ["Floral Vines", "Mini Buttis"], "6.2 meters", "640g", "Dry clean only",
         ["https://images.unsplash.com/photo-1610030469850-9655ecdd9745?w=700&auto=format&fit=crop&q=80"],
         850.0, 14.0, 68.0, 2650.0, 2650.0, 4, "GI-TN-005"),

        ("Collector Edition Vana Singaram Kanchipuram Saree", "Legendary 'Forest of Beauty' weave depicting jungle flora and fauna across whole body.",
         "Requires over 40 days of master loom execution.", "Handloom & Silk", "Kanchipuram Silk", "Tamil Nadu",
         ["Pure Silk", "Dual Tone Zari"], "Complex Jaal Weave", ["Lions", "Deer", "Peacocks", "Trees"], "6.2 meters", "990g", "Dry clean only",
         ["https://images.unsplash.com/photo-1583391733980-0010c2c2f829?w=700&auto=format&fit=crop&q=80"],
         1950.0, 36.0, 68.0, 5900.0, 5900.0, 1, "GI-TN-005")
    ]
    for p in p5:
        prod_idx = len(products) + 1
        img_url = GOOGLE_IMAGE_LINKS.get(prod_idx, f"https://encrypted-tbn0.gstatic.com/images?q=tbn:product_{prod_idx}")
        products.append((5, "Kalyanasundaram Swamy", p[0], p[1], p[2], p[2], p[3], p[4], p[5], json.dumps(p[6]), p[7], json.dumps(p[8]), p[9], p[10], p[11], json.dumps([img_url]), p[13], p[14], p[15], p[16], p[16], p[17], 0, 5, p[18], 1, json.dumps(["GI-Protected", "Kanchipuram Silk", "Korvai"]), "PUBLISHED", 85, now, now))

    # 6. Debabrata Saikia (Assam - Organic Bamboo & Cane) - 10 Products with unique bamboo/cane wicker imagery
    p6 = [
        ("Artisanal Hand-Braided Organic Bamboo Storage Basket", "100% Eco-friendly matured split bamboo living basket with spiral lattice weave.",
         "Harvested sustainably in Assam and hand-braided by indigenous master artisan Debabrata Saikia.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Organic Bamboo", "Cane Fibre"], "Cross-Weave Lattice", ["Spiral Rib", "Lattice"], "14 x 12 in", "450g", "Wipe with dry cloth",
         ["https://images.unsplash.com/photo-1590402494682-cd3fb53b1f70?w=700&auto=format&fit=crop&q=80"],
         150.0, 6.0, 58.0, 750.0, 750.0, 10, None),

        ("Handcrafted Bamboo Fruit Serving Platter Tray", "Oval serving tray with reinforced rim made from hand-sliced bamboo strands.",
         "Zero plastic food-safe natural finish with organic resin.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Matured Bamboo Splits", "Natural Resin"], "Fine Ribbed Braid", ["Oval Rim", "Linear Weave"], "16 x 10 in", "320g", "Wipe clean",
         ["https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=700&auto=format&fit=crop&q=80"],
         130.0, 5.0, 58.0, 620.0, 620.0, 12, None),

        ("Hand-Woven Cane Hanging Chandelier Lampshade", "Warm ambient lighting pendant lampshade casting geometric shadow patterns.",
         "Crafted from natural North-East Assam river cane.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Assam River Cane", "Bamboo Frame"], "Open Geometric Lattice", ["Diamond Pattern", "Cylindrical Shade"], "12 x 10 in", "410g", "Dust with soft brush",
         ["https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=700&auto=format&fit=crop&q=80"],
         220.0, 7.0, 58.0, 980.0, 980.0, 6, None),

        ("Eco-Friendly Bamboo Desktop Organizer Set", "3-piece desk accessory set for pens, stationery, and cards in natural bamboo.",
         "Sustainable zero-plastic office decor crafted by rural SHG artisans.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Organic Bamboo Slices"], "Solid Hand-Joinery", ["Minimalist Slats"], "8 x 4 x 4 in", "380g", "Wipe dry",
         ["https://images.unsplash.com/photo-1590402494580-cd3fb53b1f70?w=700&auto=format&fit=crop&q=80"],
         140.0, 4.5, 58.0, 640.0, 640.0, 8, None),

        ("Bamboo & Jute Laundry Storage Hamper", "Large capacity foldable laundry hamper with breathable woven cane walls.",
         "Natural moisture-resistant storage for sustainable homes.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Matured Bamboo", "Natural Jute"], "Spiral Interweave", ["Cylinder Walls", "Cane Lid"], "22 x 14 in", "850g", "Keep well ventilated",
         ["https://images.unsplash.com/photo-1513519245100-0e12902e5a38?w=700&auto=format&fit=crop&q=80"],
         290.0, 9.0, 58.0, 1250.0, 1250.0, 5, None),

        ("Handwoven Bamboo Bread & Snack Serving Basket (Set of 2)", "Shallow circular snack baskets with delicate braided flower rim.",
         "Ideal for serving rotis, breads, and dry fruits in eco-friendly style.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Organic Bamboo"], "Braided Edge Weave", ["Radial Sunburst", "Flower Rim"], "9 in (Dia) each", "240g", "Wipe with damp cloth",
         ["https://images.unsplash.com/photo-1590402494600-cd3fb53b1f70?w=700&auto=format&fit=crop&q=80"],
         120.0, 4.0, 58.0, 550.0, 550.0, 15, None),

        ("Cane Floor Standing Planter Pot", "Mid-century style indoor plant stand handcrafted with sturdy whole cane stems.",
         "Adds earthy organic warmth to modern living room interiors.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Thick Assam Cane", "Bamboo Base"], "Tied Joint Construction", ["Tripod Legs", "Basket Holder"], "18 in (H) x 10 in (Dia)", "680g", "Indoor use",
         ["https://images.unsplash.com/photo-1507473885800-e6ed057f782c?w=700&auto=format&fit=crop&q=80"],
         260.0, 8.0, 58.0, 1120.0, 1120.0, 6, None),

        ("Bamboo Tea Coaster & Trivet Set with Box", "Set of 6 heat-insulating round coasters packed inside matching woven box.",
         "Protects wooden tables with 100% natural organic heat resistance.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Bamboo Slices", "Cane Wire"], "Cross Hatch Weave", ["Square Box", "Round Trivets"], "4 in (Dia) each", "290g", "Wipe clean",
         ["https://images.unsplash.com/photo-1590402494620-cd3fb53b1f70?w=700&auto=format&fit=crop&q=80"],
         110.0, 3.5, 58.0, 480.0, 480.0, 20, None),

        ("Artisanal Handwoven Bamboo Tissue Box Cover", "Square tissue dispenser box with bottom sliding latch in fine cane lattice.",
         "Elegant zero-plastic bathroom and dining table accessory.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Fine Split Bamboo"], "Tight Plain Weave", ["Top Oval Slot", "Reinforced Edge"], "5 x 5 x 5 in", "210g", "Dust clean",
         ["https://images.unsplash.com/photo-1513519245120-0e12902e5a38?w=700&auto=format&fit=crop&q=80"],
         130.0, 4.0, 58.0, 580.0, 580.0, 10, None),

        ("Hand-Braided Bamboo Wall Fan & Decor Piece", "Traditional hand fan (Bisoni) embellished with colorful organic thread bindings.",
         "Can be mounted as bohemian wall art or used for refreshing breeze.", "Sustainable Crafts", "Bamboo & Cane", "Assam",
         ["Fine Bamboo Strands", "Cotton Threads"], "Decorative Twill Weave", ["Peacock Fan Fanout", "Wooden Handle"], "12 x 15 in", "160g", "Hang or dust",
         ["https://images.unsplash.com/photo-1507473885850-e6ed057f782c?w=700&auto=format&fit=crop&q=80"],
         100.0, 3.0, 58.0, 420.0, 420.0, 14, None)
    ]
    for p in p6:
        prod_idx = len(products) + 1
        img_url = GOOGLE_IMAGE_LINKS.get(prod_idx, f"https://encrypted-tbn0.gstatic.com/images?q=tbn:product_{prod_idx}")
        products.append((6, "Debabrata Saikia", p[0], p[1], p[2], p[2], p[3], p[4], p[5], json.dumps(p[6]), p[7], json.dumps(p[8]), p[9], p[10], p[11], json.dumps([img_url]), p[13], p[14], p[15], p[16], p[16], p[17], 0, 2, p[18], 0, json.dumps(["100% Eco-Friendly", "Plastic-Free", "Zero-Waste"]), "PUBLISHED", 48, now, now))

    # 7. Moumita Banerjee (West Bengal - Kantha Embroidery) - 10 Products with unique embroidered textile imagery
    p7 = [
        ("Santiniketan Handcrafted Kantha Embroidered Silk Dupatta", "Pure Tussar Silk dupatta featuring folkloric village life embroidered in thousands of running stitches.",
         "Stitched by rural women artisans led by master craftswoman Moumita Banerjee.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Pure Tussar Silk", "Cotton Threads"], "Nakshi Kantha Stitch", ["Village Life", "Alpona", "Paisley"], "2.5 m x 36 in", "280g", "Dry clean only",
         ["https://images.unsplash.com/photo-1509631179647-0177331693ae?w=700&auto=format&fit=crop&q=80"],
         500.0, 16.0, 55.0, 1950.0, 1950.0, 4, "GI-WB-006"),

        ("Nakshi Kantha Hand-Stitched Tussar Silk Saree", "Collector edition pure Tussar silk saree covered in all-over folkloric needlework.",
         "Took 45 days of patient hand-embroidery by master artisans in Birbhum.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Pure Tussar Silk", "Silk Embroidery Threads"], "All-over Running Stitch", ["Tree of Harmony", "Dancing Peacocks", "Lotus"], "6.3 meters", "650g", "Dry clean only",
         ["https://images.unsplash.com/photo-1610030469668-9655ecdd9745?w=700&auto=format&fit=crop&q=80"],
         1100.0, 32.0, 55.0, 3600.0, 3600.0, 2, "GI-WB-006"),

        ("Kantha Embroidered Silk Stole & Scarf", "Multicolor floral running stitch border on lightweight handspun silk.",
         "Versatile all-season scarf adding artisanal Bengali charm to any outfit.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Handspun Silk", "Organic Dyes"], "Fine Kantha Stitching", ["Floral Vines", "Sunburst Edges"], "2 m x 24 in", "190g", "Dry clean",
         ["https://images.unsplash.com/photo-1509631179600-0177331693ae?w=700&auto=format&fit=crop&q=80"],
         350.0, 10.0, 55.0, 1250.0, 1250.0, 6, "GI-WB-006"),

        ("Folk Village Life Kantha Wall Hanging Tapestry", "Decorative fabric tapestry depicting Bengal rural fairs, baul singers, and boats.",
         "Lined with organic cotton backing and hanging loops.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Tussar Silk & Cotton Backing"], "Narrative Needlework", ["Baul Singer", "River Boat", "Village Huts"], "36 x 24 in", "340g", "Dry clean or dust",
         ["https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=700&auto=format&fit=crop&q=80"],
         420.0, 14.0, 55.0, 1650.0, 1650.0, 3, "GI-WB-006"),

        ("Handcrafted Kantha Cushion Covers (Set of 2)", "Square sofa cushion covers with intricate geometric alpona motifs.",
         "Zippered closure with durable pure cotton-silk blended fabric.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Cotton-Silk Blend", "Cotton Embroidery"], "Alpona Geometric Stitch", ["Circular Alpona", "Corner Floral"], "16 x 16 in each", "310g", "Hand wash gentle",
         ["https://images.unsplash.com/photo-1509631179620-0177331693ae?w=700&auto=format&fit=crop&q=80"],
         260.0, 7.0, 55.0, 920.0, 920.0, 8, "GI-WB-006"),

        ("Royal Blue Paisley Motif Kantha Silk Dupatta", "Vibrant royal blue Tussar silk embroidered with yellow and red paisley cones.",
         "Generational women empowerment initiative in Santiniketan.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Pure Silk", "Colorfast Threads"], "Paisley Fill Stitch", ["Kalka (Paisley)", "Lotus Border"], "2.5 m", "270g", "Dry clean only",
         ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
         480.0, 15.0, 55.0, 1850.0, 1850.0, 4, "GI-WB-006"),

        ("Indigo Dabu Print & Kantha Stitched Jacket Fabric", "Hand-block printed indigo fabric enriched with running kantha textures.",
         "Tailorable fabric for bespoke artisanal ethnic jackets and vests.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Natural Indigo Cotton"], "Running Line Stitch", ["Geometric Grid", "Indigo Flora"], "2.5 meters", "420g", "Hand wash separate",
         ["https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=700&auto=format&fit=crop&q=80"],
         380.0, 11.0, 55.0, 1380.0, 1380.0, 5, "GI-WB-006"),

        ("Kantha Embroidered Evening Clutch Purse", "Handheld silk clutch purse with magnetic flap and detachable metal chain.",
         "Embroidered with delicate bird motifs for wedding celebrations.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Silk Outer", "Metal Chain", "Satin Lining"], "Fine Detail Needlework", ["Bird Pair", "Floral Spray"], "8 x 5 in", "210g", "Spot clean",
         ["https://images.unsplash.com/photo-1509631179640-0177331693ae?w=700&auto=format&fit=crop&q=80"],
         220.0, 6.0, 55.0, 780.0, 780.0, 9, "GI-WB-006"),

        ("Black & Gold Royal Kantha Silk Saree", "Dramatic black Tussar silk embellished with shimmering golden and cream kantha threads.",
         "High-fashion evening statement saree celebrating Bengal heritage.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Black Tussar Silk", "Gold Thread"], "Contrast Needlework", ["Royal Kalas", "Floral Jaal"], "6.3 meters", "660g", "Dry clean only",
         ["https://images.unsplash.com/photo-1609357605129-26f69add5d6e?w=700&auto=format&fit=crop&q=80"],
         1050.0, 30.0, 55.0, 3450.0, 3450.0, 3, "GI-WB-006"),

        ("Floral Garden Kantha Table Runner", "Long dining table runner decorated with central floral vine and scalloped borders.",
         "Adds warm handcrafted elegance to dinner tables.", "Handloom & Textiles", "Kantha Embroidery", "West Bengal",
         ["Heavy Cotton Linen", "Embroidery Threads"], "Symmetric Vine Stitch", ["Lotus Blossom", "Scroll Vines"], "60 x 14 in", "360g", "Gentle wash",
         ["https://images.unsplash.com/photo-1509631179660-0177331693ae?w=700&auto=format&fit=crop&q=80"],
         290.0, 8.0, 55.0, 1020.0, 1020.0, 7, "GI-WB-006")
    ]
    for p in p7:
        prod_idx = len(products) + 1
        img_url = GOOGLE_IMAGE_LINKS.get(prod_idx, f"https://encrypted-tbn0.gstatic.com/images?q=tbn:product_{prod_idx}")
        products.append((7, "Moumita Banerjee", p[0], p[1], p[2], p[2], p[3], p[4], p[5], json.dumps(p[6]), p[7], json.dumps(p[8]), p[9], p[10], p[11], json.dumps([img_url]), p[13], p[14], p[15], p[16], p[16], p[17], 0, 4, p[18], 1, json.dumps(["GI-Protected", "Tussar Silk", "Nakshi Kantha"]), "PUBLISHED", 60, now, now))

    # 8. Ghulam Mohammad Mir (Jammu & Kashmir - Pashmina Cashmere) - 10 Products with unique cashmere shawl imagery
    p8 = [
        ("Royal Handspun Kashmiri Pashmina Cashmere Shawl", "Pure 100% Changthangi goat cashmere woven on traditional handloom with delicate sozni needlework.",
         "Ultra-soft 12-micron royal cashmere that passes effortlessly through a finger ring.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["100% Pure Cashmere", "Natural Dyes"], "Hand-Spun Fine Weave & Sozni", ["Chinar Leaf", "Paisley", "Floral Jaal"], "2 x 1 meter", "190g", "Dry clean only",
         ["https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=700&auto=format&fit=crop&q=80"],
         2000.0, 24.0, 75.0, 5600.0, 5600.0, 2, "GI-JK-007"),

        ("Chinar Leaf Hand-Embroidered Pashmina Shawl", "Autumn Chinar maple leaf motifs embroidered along borders in gold and crimson silk floss.",
         "Woven by master artisan Ghulam Mohammad Mir in downtown Srinagar.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["Changthangi Cashmere", "Silk Floss"], "Sozni Needlework", ["Chinar Leaf Border", "Corner Hashiya"], "2 x 1 meter", "200g", "Dry clean only",
         ["https://images.unsplash.com/photo-1606760227050-3dd870d97f1d?w=700&auto=format&fit=crop&q=80"],
         2200.0, 28.0, 75.0, 6200.0, 6200.0, 2, "GI-JK-007"),

        ("Classic Natural Ivory Solid Pashmina Wrap", "Undyed pure ivory cashmere wrap showcasing natural feather-soft cloud texture.",
         "Versatile timeless luxury companion for chilly winter evenings.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["100% Undyed Cashmere"], "Diamond Weave (Chashm-e-Bulbul)", ["Subtle Diamond Grain", "Eyelash Fringe"], "2 x 1 meter", "175g", "Dry clean only",
         ["https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=700&auto=format&fit=crop&q=80"],
         1600.0, 18.0, 75.0, 4500.0, 4500.0, 3, "GI-JK-007"),

        ("Reversible Kani Weave Pashmina Shawl", "Intricate Kani technique using tiny wooden spools (Tujis) to interweave colored yarns.",
         "Museum-grade artisanal treasure requiring 3 months on handloom.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["Pure Cashmere Wool", "Vegetable Dyes"], "Kani Twill Tapestry Weave", ["Mughal Floral Bouquet", "Paisley Medallions"], "2 x 1 meter", "220g", "Dry clean only",
         ["https://images.unsplash.com/photo-1606760227070-3dd870d97f1d?w=700&auto=format&fit=crop&q=80"],
         2800.0, 40.0, 75.0, 7800.0, 7800.0, 1, "GI-JK-007"),

        ("Paisley Floral Jaal All-Over Sozni Pashmina", "Exquisite all-over needlework dense jaal covering the entire cashmere surface.",
         "Incredible warmth and ethereal lightness verified under GI seal.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["100% Pashmina Cashmere"], "All-Over Sozni Jaal", ["Badam Paisley", "Rose Buds", "Vines"], "2 x 1 meter", "215g", "Dry clean only",
         ["https://images.unsplash.com/photo-1606760227090-3dd870d97f1d?w=700&auto=format&fit=crop&q=80"],
         2600.0, 35.0, 75.0, 7200.0, 7200.0, 1, "GI-JK-007"),

        ("Turquoise Blue Sozni Border Pashmina Stole", "Vibrant turquoise blue pure cashmere stole with fine silver-grey sozni border.",
         "Perfect compact size for daily luxury drape.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["Pure Cashmere", "Silk Threads"], "Fine Border Needlework", ["Border Waves", "Corner Boota"], "2 m x 28 in", "140g", "Dry clean only",
         ["https://images.unsplash.com/photo-1509631179647-0177331693ae?w=700&auto=format&fit=crop&q=80"],
         1200.0, 14.0, 75.0, 3400.0, 3400.0, 4, "GI-JK-007"),

        ("Midnight Black & Gold Tilla Embroidered Pashmina", "Metallic gold Tilla threadwork on pitch black pure cashmere shawl.",
         "Royal bridal shawl worn for grand evening banquets.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["Pashmina Cashmere", "Gold Tilla Wire"], "Tilla Hand Needlework", ["Mughal Arch", "Floral Paisley Border"], "2 x 1 meter", "240g", "Dry clean only",
         ["https://images.unsplash.com/photo-1606760227080-3dd870d97f1d?w=700&auto=format&fit=crop&q=80"],
         2400.0, 32.0, 75.0, 6800.0, 6800.0, 2, "GI-JK-007"),

        ("Vintage Walnut Husk Dyed Brown Pashmina Shawl", "Dyed organically with local Kashmiri walnut shells for earthy brown tones.",
         "100% chemical-free organic vegetable dyeing process.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["Pure Cashmere", "Walnut Dye"], "Twill Weave Handloom", ["Solid Body", "Self Fringes"], "2 x 1 meter", "185g", "Dry clean only",
         ["https://images.unsplash.com/photo-1583391733975-0010c2c2f829?w=700&auto=format&fit=crop&q=80"],
         1500.0, 16.0, 75.0, 4200.0, 4200.0, 3, "GI-JK-007"),

        ("Ruby Crimson Kashmiri Cashmere Scarf", "Rich ruby crimson scarf with delicate micro-sozni embroidered corners.",
         "Unisex winter luxury certified by Craft Development Institute.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["Pure Pashmina Cashmere"], "Micro Needlework", ["Four-Corner Bootis"], "1.8 m x 22 in", "125g", "Dry clean only",
         ["https://images.unsplash.com/photo-1606760227060-3dd870d97f1d?w=700&auto=format&fit=crop&q=80"],
         950.0, 11.0, 75.0, 2750.0, 2750.0, 5, "GI-JK-007"),

        ("Kashmir Heritage Shahkaar Pashmina Shawl", "Ultra-fine weave with 108 distinct flower varieties hand-embroidered in border.",
         "The pinnacle of Kashmiri needlecraft artistry and wage protection.", "Luxury Handloom", "Pashmina Cashmere", "Jammu & Kashmir",
         ["Grade-A Changthangi Cashmere"], "Fine Sozni Embroidery", ["108 Flower Hashiya", "Paisley Medallions"], "2 x 1 meter", "210g", "Dry clean only",
         ["https://images.unsplash.com/photo-1606760227040-3dd870d97f1d?w=700&auto=format&fit=crop&q=80"],
         3200.0, 48.0, 75.0, 8900.0, 8900.0, 1, "GI-JK-007")
    ]
    for p in p8:
        prod_idx = len(products) + 1
        img_url = GOOGLE_IMAGE_LINKS.get(prod_idx, f"https://encrypted-tbn0.gstatic.com/images?q=tbn:product_{prod_idx}")
        products.append((8, "Ghulam Mohammad Mir", p[0], p[1], p[2], p[2], p[3], p[4], p[5], json.dumps(p[6]), p[7], json.dumps(p[8]), p[9], p[10], p[11], json.dumps([img_url]), p[13], p[14], p[15], p[16], p[16], p[17], 0, 6, p[18], 1, json.dumps(["GI-Protected", "Pashmina", "Cashmere", "Handspun"]), "PUBLISHED", 95, now, now))

    return products


def seed_database(force: bool = False):
    conn = get_connection()
    cursor = conn.cursor()

    if not force:
        cursor.execute("SELECT COUNT(*) as count FROM products")
        if cursor.fetchone()["count"] >= 80:
            conn.close()
            return

    # Clear existing tables for fresh multi-persona seed
    tables = ["users", "artisans", "buyers", "wage_rules", "gi_records", "products", "orders", "escrow_records", "tracking_events", "messages", "notifications", "reviews", "audit_logs", "demand_forecasts"]
    for t in tables:
        cursor.execute(f"DELETE FROM {t}")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{t}'")

    now = datetime.utcnow().isoformat()

    # 1. Users
    users = [
        ("ARTISAN", "Rishikant Mishra", "DEMO-ARTISAN-001", "rishikant.mishra@example.test", "+91 98765 43210", "Maharashtra", "Nashik"),
        ("ARTISAN", "Meenakshi Jha", "DEMO-ARTISAN-002", "meenakshi.jha@example.test", "+91 98765 43211", "Bihar", "Madhubani"),
        ("ARTISAN", "Devendra Sharma", "DEMO-ARTISAN-003", "devendra.sharma@example.test", "+91 98765 43212", "Rajasthan", "Jaipur"),
        ("ARTISAN", "Gurucharan Mohapatra", "DEMO-ARTISAN-004", "gurucharan.m@example.test", "+91 98765 43213", "Odisha", "Mayurbhanj"),
        ("ARTISAN", "Kalyanasundaram Swamy", "DEMO-ARTISAN-005", "kalyanasundaram.s@example.test", "+91 98765 43214", "Tamil Nadu", "Kanchipuram"),
        ("ARTISAN", "Debabrata Saikia", "DEMO-ARTISAN-006", "debabrata.s@example.test", "+91 98765 43215", "Assam", "Guwahati"),
        ("ARTISAN", "Moumita Banerjee", "DEMO-ARTISAN-007", "moumita.b@example.test", "+91 98765 43216", "West Bengal", "Santiniketan"),
        ("ARTISAN", "Ghulam Mohammad Mir", "DEMO-ARTISAN-008", "ghulam.mir@example.test", "+91 98765 43217", "Jammu & Kashmir", "Srinagar"),
        
        ("BUYER", "Rajesh Kumar", "DEMO-BUYER-001", "rajesh.k@example.test", "+91 98111 22334", "Karnataka", "Bengaluru"),
        ("BUYER", "Priya Sharma", "DEMO-BUYER-002", "priya.s@example.test", "+91 98222 33445", "Maharashtra", "Mumbai"),
        ("BUYER", "Amit Verma", "DEMO-BUYER-003", "amit.v@example.test", "+91 98333 44556", "Delhi", "New Delhi"),
        ("BUYER", "Deepa Nair", "DEMO-BUYER-004", "deepa.n@example.test", "+91 98444 55667", "Kerala", "Kochi"),
        ("BUYER", "Vikram Mehta", "DEMO-BUYER-005", "vikram.m@example.test", "+91 98555 66778", "Gujarat", "Ahmedabad"),
        ("BUYER", "Sneha Mukherjee", "DEMO-BUYER-006", "sneha.m@example.test", "+91 98666 77889", "West Bengal", "Kolkata"),
        
        ("ADMIN", "SIH Admin Official", "DEMO-ADMIN-001", "admin@sih-artisan.gov.in", "+91 99000 11223", "Delhi", "New Delhi")
    ]
    cursor.executemany("""
    INSERT INTO users (role, name, identifier, email, mobile, state, district, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [(u[0], u[1], u[2], u[3], u[4], u[5], u[6], now) for u in users])

    # 2. Artisans
    artisans = [
        (1, "Rishikant Mishra", "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&auto=format&fit=crop&q=80",
         "Maharashtra", "Nashik", "Yeola", "Handloom & Silk", "Paithani Weaving", 18,
         json.dumps(["Marathi", "Hindi"]), "PMV-MH-2024-8841", "Yeola Paithani Weavers Guild", "Maharashtra State Handloom Fed",
         "VERIFIED", "Statutory wage verified via Bhashini voice submission. GI verified.", "••••••••4821", 4.95, 24,
         "Fourth generation handloom weaver from Yeola specializing in pure silk and peacock zari motifs.", now),
        
        (2, "Meenakshi Jha", "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&auto=format&fit=crop&q=80",
         "Bihar", "Madhubani", "Ranti", "Folk Art & Decor", "Madhubani Painting", 14,
         json.dumps(["Maithili", "Hindi"]), "PMV-BR-2024-3912", "Mithila Folk Artists Union", "Jitwarpur Artisan SHG",
         "VERIFIED", "Mithila GI certified. All natural vegetable dyes authenticated.", "••••••••5519", 4.88, 19,
         "Folk artist painting sacred mythological stories on handmade paper using bamboo twigs.", now),

        (3, "Devendra Sharma", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&auto=format&fit=crop&q=80",
         "Rajasthan", "Jaipur", "Kot Jewar", "Ceramics & Decor", "Jaipur Blue Pottery", 22,
         json.dumps(["Hindi", "Rajasthani"]), "PMV-RJ-2023-9014", "Jaipur Blue Pottery Artisans Trust", "Rajasthan Handicrafts Coop",
         "VERIFIED", "Authentic quartz-glass composite verification complete. No clay utilized.", "••••••••1923", 4.91, 31,
         "Master artisan preserving the royal 14th century quartz stone pottery tradition.", now),

        (4, "Gurucharan Mohapatra", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&auto=format&fit=crop&q=80",
         "Odisha", "Mayurbhanj", "Bastar Border", "Metallurgy & Sculpture", "Dhokra Lost-Wax Art", 16,
         json.dumps(["Odia", "Hindi"]), "PMV-OD-2024-6721", "Bastar Tribal Guild", "Tribal Cooperative Marketing Fed (TRIFED)",
         "VERIFIED", "Prehistoric Harappan lost-wax casting technique certified.", "••••••••8812", 4.97, 15,
         "Tribal master crafting brass and bell metal casting through ancient beeswax molds.", now),

        (5, "Kalyanasundaram Swamy", "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&auto=format&fit=crop&q=80",
         "Tamil Nadu", "Kanchipuram", "Pillayar Palayam", "Handloom & Silk", "Kanchipuram Silk Weaving", 25,
         json.dumps(["Tamil", "English"]), "PMV-TN-2024-5512", "Kanchipuram Silk Weavers Society", "Tamil Nadu Zari Board",
         "VERIFIED", "Korvai interlocking temple border and pure silver zari certified.", "••••••••7731", 4.96, 28,
         "Master pitloom weaver specializing in pure mulberry silk with solid temple borders.", now),

        (6, "Debabrata Saikia", "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&auto=format&fit=crop&q=80",
         "Assam", "Guwahati", "Barpeta", "Sustainable Crafts", "Organic Bamboo & Cane", 12,
         json.dumps(["Assamese", "Hindi"]), "PMV-AS-2024-3321", "Assam Cane & Bamboo Crafts Guild", "North East Handicrafts Corp",
         "VERIFIED", "Sustainable forest-harvested bamboo certified zero-plastic.", "••••••••2284", 4.85, 14,
         "Indigenous artisan creating fine hand-braided organic bamboo living accessories.", now),

        (7, "Moumita Banerjee", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&auto=format&fit=crop&q=80",
         "West Bengal", "Birbhum", "Santiniketan", "Handloom & Textiles", "Kantha Hand Embroidery", 15,
         json.dumps(["Bengali", "English", "Hindi"]), "PMV-WB-2024-4419", "Santiniketan Crafts Collective", "West Bengal Tantuja",
         "VERIFIED", "Traditional running stitch Kantha embroidery on pure Tussar silk.", "••••••••9042", 4.92, 21,
         "Needlecraft artist crafting intricate rural folkloric tapestries and dupattas.", now),

        (8, "Ghulam Mohammad Mir", "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&auto=format&fit=crop&q=80",
         "Jammu & Kashmir", "Srinagar", "Downtown", "Luxury Handloom", "Pashmina Cashmere Shawl", 30,
         json.dumps(["Kashmiri", "Urdu", "English"]), "PMV-JK-2024-1188", "Kashmir Pashmina Artisans Union", "Craft Development Institute",
         "VERIFIED", "Authentic 12-micron Changthangi mountain cashmere verified under GI tag.", "••••••••6618", 4.99, 18,
         "Fifth generation master artisan hand-spinning and weaving royal Pashmina sozni shawls.", now)
    ]
    cursor.executemany("""
    INSERT INTO artisans (user_id, name, profile_photo, state_cluster, district, village_city, craft_category, specific_craft,
        years_experience, languages, vishwakarma_id, gi_association, cooperative_association, verification_status,
        verification_notes, bank_masked, rating, verified_orders_count, story, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, artisans)

    # 3. Buyers
    buyers = [
        (9, "Rajesh Kumar", "+91 98111 22334", "rajesh.k@example.test", "Flat 402, Green Glen Layout, Bellandur", "560103", now),
        (10, "Priya Sharma", "+91 98222 33445", "priya.s@example.test", "B-12, Sea Pearl Apt, Bandra West", "400050", now),
        (11, "Amit Verma", "+91 98333 44556", "amit.v@example.test", "14/2 Connaught Place, New Delhi", "110001", now),
        (12, "Deepa Nair", "+91 98444 55667", "deepa.n@example.test", "Palm Grove Villa, Kakkanad, Kochi", "682030", now),
        (13, "Vikram Mehta", "+91 98555 66778", "vikram.m@example.test", "701 heritage heights, Bodakdev, Ahmedabad", "380054", now),
        (14, "Sneha Mukherjee", "+91 98666 77889", "sneha.m@example.test", "45/A Lake Road, Ballygunge, Kolkata", "700029", now)
    ]
    cursor.executemany("""
    INSERT INTO buyers (user_id, name, mobile, email, default_address, default_pincode, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, buyers)

    # 4. Wage Rules
    wage_rules = [
        ("Maharashtra", "Paithani Weaving", "Master Craftsman", 520.0, 65.0, "2026-01-01", "MH-MIN-WAGE-SEC-12(A)/2026", now),
        ("Bihar", "Madhubani Painting", "Skilled Folk Artist", 496.0, 62.0, "2026-01-01", "BR-MIN-WAGE-NOTIF-44/2026", now),
        ("Rajasthan", "Jaipur Blue Pottery", "Skilled Ceramicist", 520.0, 65.0, "2026-01-01", "RJ-LABOUR-CIRC-881/2026", now),
        ("Odisha", "Dhokra Bell Metal", "Skilled Metallurgist", 480.0, 60.0, "2026-01-01", "OD-TRIBAL-CRAFT-BENCHMARK-03", now),
        ("Tamil Nadu", "Kanchipuram Silk", "Master Handloom Weaver", 544.0, 68.0, "2026-01-01", "TN-HANDLOOM-WAGE-SCHEDULE-B", now),
        ("Assam", "Bamboo & Cane Weaving", "Skilled Artisan", 464.0, 58.0, "2026-01-01", "AS-FOREST-CRAFT-SCALE-09", now),
        ("West Bengal", "Kantha Embroidery", "Skilled Needlecraft", 440.0, 55.0, "2026-01-01", "WB-MIN-WAGE-SCHEDULE-C", now),
        ("Jammu & Kashmir", "Pashmina Weaving", "Master Weaver", 600.0, 75.0, "2026-01-01", "JK-HANDICRAFT-NOTIF-02/2026", now),
        ("Uttar Pradesh", "Chikan Embroidery", "Skilled Embroiderer", 440.0, 55.0, "2026-01-01", "UP-LABOUR-MIN-NOTIF-2026", now)
    ]
    cursor.executemany("""
    INSERT INTO wage_rules (state_name, craft_name, skill_level, daily_wage, hourly_rate, effective_date, statutory_reference, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, wage_rules)

    # 5. GI Records
    gi_records = [
        ("GI-MH-001", "Paithani Sarees and Fabrics", "Maharashtra", "Handloom & Textiles", "Yeola Paithani Weavers Guild", 2010, "VERIFIED", "https://ipindiaservices.gov.in/gi/mh001", now),
        ("GI-BR-002", "Madhubani Paintings", "Bihar", "Folk Art & Decor", "Mithila Folk Artists Union", 2007, "VERIFIED", "https://ipindiaservices.gov.in/gi/br002", now),
        ("GI-RJ-003", "Blue Pottery of Jaipur", "Rajasthan", "Ceramics & Decor", "Jaipur Blue Pottery Artisans Trust", 2008, "VERIFIED", "https://ipindiaservices.gov.in/gi/rj003", now),
        ("GI-OD-004", "Odisha Dhokra Craft", "Odisha", "Metal Craft & Sculpture", "Bastar & Mayurbhanj Tribal Society", 2018, "VERIFIED", "https://ipindiaservices.gov.in/gi/od004", now),
        ("GI-TN-005", "Kanchipuram Silk", "Tamil Nadu", "Handloom & Silk", "Kanchipuram Silk Weavers Society", 2005, "VERIFIED", "https://ipindiaservices.gov.in/gi/tn005", now),
        ("GI-WB-006", "Nakshi Kantha", "West Bengal", "Handloom & Textiles", "Santiniketan Crafts Collective", 2008, "VERIFIED", "https://ipindiaservices.gov.in/gi/wb006", now),
        ("GI-JK-007", "Kashmir Pashmina", "Jammu & Kashmir", "Luxury Handloom", "Kashmir Pashmina Artisans Union", 2008, "VERIFIED", "https://ipindiaservices.gov.in/gi/jk007", now)
    ]
    cursor.executemany("""
    INSERT INTO gi_records (gi_number, craft_name, region_state, category, authorized_association, registered_year, status, certificate_url, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, gi_records)

    # 6. Full 80 Products (10 for each of the 8 Artisans)
    all_products = generate_full_products_catalog(now)
    cursor.executemany("""
    INSERT INTO products (artisan_id, artisan_name, title, short_description, description, heritage_story, category,
        craft_type, state_cluster, materials, technique, motifs, dimensions, weight, care_instructions, image_urls,
        material_cost, labor_hours, hourly_wage_rate, suggested_fair_price, selling_price, stock_quantity,
        is_made_to_order, production_days, gi_number, gi_verified, tags, status, view_count, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, all_products)

    # 7. Sample Orders linking different buyers to respective artisans
    orders = [
        ("ORD-2026-8819", 1, "Authentic Handwoven Paithani Silk Saree",
         GOOGLE_IMAGE_LINKS.get(1, "/static/images/product_1.svg"),
         1, "Rishikant Mishra", 1, "Rajesh Kumar", "+91 98111 22334",
         "Flat 402, Green Glen Layout, Bellandur", "560103", "Bengaluru", "Karnataka",
         1, 2344.0, 2344.0, 975.0, 800.0, 150.0, 50.0,
         "DEMO_UPI_ESCROW", "AUTHORIZED", "DISPATCHED",
         "India Post SpeedPost (ONDC Logistics)", "IP-IN-889921447",
         (datetime.utcnow() + timedelta(days=2)).strftime("%d %b %Y"),
         (datetime.utcnow() - timedelta(days=2)).isoformat(), now),

        ("ORD-2026-7721", 11, "Traditional Madhubani Mithila Tree of Life Painting",
         GOOGLE_IMAGE_LINKS.get(11, "/static/images/product_11.svg"),
         2, "Meenakshi Jha", 2, "Priya Sharma", "+91 98222 33445",
         "B-12, Sea Pearl Apt, Bandra West", "400050", "Mumbai", "Maharashtra",
         1, 1220.0, 1220.0, 496.0, 350.0, 100.0, 40.0,
         "DEMO_UPI_ESCROW", "AUTHORIZED", "ESCROW_RELEASED",
         "India Post SpeedPost (ONDC Logistics)", "IP-IN-332119904",
         (datetime.utcnow() - timedelta(days=1)).strftime("%d %b %Y"),
         (datetime.utcnow() - timedelta(days=5)).isoformat(), now),

        ("ORD-2026-6632", 21, "Handcrafted Jaipur Blue Pottery Floral Motif Vase",
         GOOGLE_IMAGE_LINKS.get(21, "/static/images/product_21.svg"),
         3, "Devendra Sharma", 3, "Amit Verma", "+91 98333 44556",
         "14/2 Connaught Place, New Delhi", "110001", "New Delhi", "Delhi",
         1, 815.0, 815.0, 325.0, 200.0, 100.0, 25.0,
         "DEMO_UPI_ESCROW", "AUTHORIZED", "PAYMENT_SECURED",
         "India Post SpeedPost (ONDC Logistics)", "IP-IN-554412389",
         (datetime.utcnow() + timedelta(days=3)).strftime("%d %b %Y"),
         (datetime.utcnow() - timedelta(hours=6)).isoformat(), now),

        ("ORD-2026-5541", 31, "Tribal Dhokra Lost-Wax Bell Metal Dancing Figurine",
         GOOGLE_IMAGE_LINKS.get(31, "/static/images/product_31.svg"),
         4, "Gurucharan Mohapatra", 4, "Deepa Nair", "+91 98444 55667",
         "Palm Grove Villa, Kakkanad, Kochi", "682030", "Kochi", "Kerala",
         1, 2425.0, 2425.0, 1080.0, 600.0, 150.0, 60.0,
         "DEMO_UPI_ESCROW", "AUTHORIZED", "CRAFTING",
         "India Post SpeedPost (ONDC Logistics)", "IP-IN-776655123",
         (datetime.utcnow() + timedelta(days=4)).strftime("%d %b %Y"),
         (datetime.utcnow() - timedelta(days=1)).isoformat(), now),

        ("ORD-2026-4410", 41, "Pure Zari Handwoven Kanchipuram Temple Border Silk Saree",
         GOOGLE_IMAGE_LINKS.get(41, "/static/images/product_41.svg"),
         5, "Kalyanasundaram Swamy", 5, "Vikram Mehta", "+91 98555 66778",
         "701 heritage heights, Bodakdev, Ahmedabad", "380054", "Ahmedabad", "Gujarat",
         1, 3850.0, 3850.0, 1496.0, 1200.0, 150.0, 90.0,
         "DEMO_UPI_ESCROW", "AUTHORIZED", "ARTISAN_ACCEPTED",
         "India Post SpeedPost (ONDC Logistics)", "IP-IN-998811223",
         (datetime.utcnow() + timedelta(days=5)).strftime("%d %b %Y"),
         (datetime.utcnow() - timedelta(hours=18)).isoformat(), now),

        ("ORD-2026-3325", 51, "Artisanal Hand-Braided Organic Bamboo Storage Basket",
         GOOGLE_IMAGE_LINKS.get(51, "/static/images/product_51.svg"),
         6, "Debabrata Saikia", 6, "Sneha Mukherjee", "+91 98666 77889",
         "45/A Lake Road, Ballygunge, Kolkata", "700029", "Kolkata", "West Bengal",
         1, 750.0, 750.0, 348.0, 150.0, 100.0, 20.0,
         "DEMO_UPI_ESCROW", "AUTHORIZED", "DISPATCHED",
         "India Post SpeedPost (ONDC Logistics)", "IP-IN-445566778",
         (datetime.utcnow() + timedelta(days=3)).strftime("%d %b %Y"),
         (datetime.utcnow() - timedelta(days=1)).isoformat(), now),

        ("ORD-2026-2214", 61, "Santiniketan Handcrafted Kantha Embroidered Silk Dupatta",
         GOOGLE_IMAGE_LINKS.get(61, "/static/images/product_61.svg"),
         7, "Moumita Banerjee", 1, "Rajesh Kumar", "+91 98111 22334",
         "Flat 402, Green Glen Layout, Bellandur", "560103", "Bengaluru", "Karnataka",
         1, 1950.0, 1950.0, 880.0, 500.0, 120.0, 50.0,
         "DEMO_UPI_ESCROW", "AUTHORIZED", "CRAFTING",
         "India Post SpeedPost (ONDC Logistics)", "IP-IN-221199334",
         (datetime.utcnow() + timedelta(days=4)).strftime("%d %b %Y"),
         (datetime.utcnow() - timedelta(hours=14)).isoformat(), now),

        ("ORD-2026-1108", 71, "Royal Handspun Kashmiri Pashmina Cashmere Shawl",
         GOOGLE_IMAGE_LINKS.get(71, "/static/images/product_71.svg"),
         8, "Ghulam Mohammad Mir", 2, "Priya Sharma", "+91 98222 33445",
         "B-12, Sea Pearl Apt, Bandra West", "400050", "Mumbai", "Maharashtra",
         1, 5600.0, 5600.0, 1800.0, 2000.0, 150.0, 120.0,
         "DEMO_UPI_ESCROW", "AUTHORIZED", "PAYMENT_SECURED",
         "India Post SpeedPost (ONDC Logistics)", "IP-IN-110022884",
         (datetime.utcnow() + timedelta(days=6)).strftime("%d %b %Y"),
         (datetime.utcnow() - timedelta(hours=4)).isoformat(), now)
    ]
    cursor.executemany("""
    INSERT INTO orders (order_number, product_id, product_title, product_image, artisan_id, artisan_name,
        buyer_id, buyer_name, buyer_phone, delivery_address, delivery_pincode, delivery_city, delivery_state,
        quantity, unit_price, total_amount, artisan_wage_payout, raw_material_payout, logistics_fee, platform_fee,
        payment_method, payment_status, escrow_state, carrier, tracking_number, estimated_delivery, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, orders)

    # 8. Escrow Records
    escrows = [
        (1, "ORD-2026-8819", 2344.0, 1775.0, 569.0, "HELD", (datetime.utcnow() - timedelta(days=2)).isoformat(), None, None),
        (2, "ORD-2026-7721", 1220.0, 846.0, 374.0, "RELEASED", (datetime.utcnow() - timedelta(days=5)).isoformat(), (datetime.utcnow() - timedelta(days=1)).isoformat(), "TXN_ESCROW_REL_88914"),
        (3, "ORD-2026-6632", 815.0, 525.0, 290.0, "HELD", (datetime.utcnow() - timedelta(hours=6)).isoformat(), None, None),
        (4, "ORD-2026-5541", 2425.0, 1680.0, 745.0, "HELD", (datetime.utcnow() - timedelta(days=1)).isoformat(), None, None),
        (5, "ORD-2026-4410", 3850.0, 2696.0, 1154.0, "HELD", (datetime.utcnow() - timedelta(hours=18)).isoformat(), None, None),
        (6, "ORD-2026-3325", 750.0, 498.0, 252.0, "HELD", (datetime.utcnow() - timedelta(days=1)).isoformat(), None, None),
        (7, "ORD-2026-2214", 1950.0, 1380.0, 570.0, "HELD", (datetime.utcnow() - timedelta(hours=14)).isoformat(), None, None),
        (8, "ORD-2026-1108", 5600.0, 3800.0, 1800.0, "HELD", (datetime.utcnow() - timedelta(hours=4)).isoformat(), None, None)
    ]
    cursor.executemany("""
    INSERT INTO escrow_records (order_id, order_number, total_held, artisan_share, platform_share, status, held_at, released_at, release_tx_ref)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, escrows)

    # 9. Tracking Events
    tracking_events = [
        (1, "ORDER_CREATED", "Order Placed & Escrow Created", "Buyer completed checkout on ONDC Buyer App. Escrow fund held securely.", "Bengaluru, KA", (datetime.utcnow() - timedelta(days=2, hours=4)).isoformat()),
        (1, "PAYMENT_SECURED", "Payment Secured in Trust Escrow", "₹2,344.00 locked in RBI-compliant escrow account for artisan wage safety.", "Platform Vault", (datetime.utcnow() - timedelta(days=2, hours=3)).isoformat()),
        (1, "ARTISAN_ACCEPTED", "Artisan Accepted Order", "Rishikant Mishra confirmed order specifications in Yeola cluster.", "Yeola, MH", (datetime.utcnow() - timedelta(days=2, hours=1)).isoformat()),
        (1, "QUALITY_CHECK", "GI Authenticity & Quality Verified", "Peacock pallu zari verified by cluster inspector.", "Yeola QC Center", (datetime.utcnow() - timedelta(days=1, hours=6)).isoformat()),
        (1, "DISPATCHED", "Handed over to India Post SpeedPost", "Airway Bill IP-IN-889921447 generated. En route to transit hub.", "Nashik Logistics Hub", (datetime.utcnow() - timedelta(hours=14)).isoformat()),
        
        (3, "PAYMENT_SECURED", "Payment Secured in Trust Escrow", "₹815.00 secured in Escrow. Devendra Sharma notified to begin glazing.", "Jaipur Hub", (datetime.utcnow() - timedelta(hours=6)).isoformat()),
        (4, "CRAFTING", "Lost-Wax Molding In Progress", "Gurucharan Mohapatra started lost-wax furnace casting in Mayurbhanj.", "Bastar/Mayurbhanj", (datetime.utcnow() - timedelta(hours=12)).isoformat()),
        (5, "ARTISAN_ACCEPTED", "Artisan Accepted Order", "Kalyanasundaram Swamy accepted order in Kanchipuram cluster.", "Kanchipuram, TN", (datetime.utcnow() - timedelta(hours=16)).isoformat()),
        (6, "DISPATCHED", "Dispatched via SpeedPost", "Debabrata Saikia dispatched bamboo basket from Guwahati hub.", "Guwahati, AS", (datetime.utcnow() - timedelta(hours=8)).isoformat()),
        (7, "CRAFTING", "Kantha Stitching in Progress", "Moumita Banerjee and village SHG artisans active on needlework.", "Santiniketan, WB", (datetime.utcnow() - timedelta(hours=10)).isoformat()),
        (8, "PAYMENT_SECURED", "Pashmina Order Escrow Locked", "Ghulam Mohammad Mir notified to commence sozni embroidery.", "Srinagar, JK", (datetime.utcnow() - timedelta(hours=2)).isoformat())
    ]
    cursor.executemany("""
    INSERT INTO tracking_events (order_id, status_key, title, description, location, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, tracking_events)

    # 10. Messages
    messages = [
        (1, "artisan", "Rishikant Mishra", "Namaskar Rajesh ji! Saree ready ahe, peacock zari pallu khup sundar distoy.", "Namaskar Rajesh ji! The saree is ready, the peacock zari pallu looks beautiful.", "mr", "en", (datetime.utcnow() - timedelta(days=1, hours=2)).isoformat()),
        (1, "buyer", "Rajesh Kumar", "Thank you Savita ji! Looking forward to receiving this masterpiece for my mother's birthday.", "धन्यवाद सविता जी! माझ्या आईच्या वाढदिवसासाठी हे सुंदर वस्त्र मिळण्याची वाट पाहत आहे.", "en", "mr", (datetime.utcnow() - timedelta(days=1, hours=1)).isoformat()),
        (3, "artisan", "Devendra Sharma", "Namaste Amit ji! Quartz glaze vase firing is underway in kiln.", "Namaste Amit ji! Quartz glaze vase firing is underway in kiln.", "hi", "en", (datetime.utcnow() - timedelta(hours=4)).isoformat()),
        (4, "artisan", "Gurucharan Mohapatra", "Johar Deepa ji! Beeswax structure for the dancing figurine is completed.", "Johar Deepa ji! Beeswax structure for the dancing figurine is completed.", "hi", "en", (datetime.utcnow() - timedelta(hours=8)).isoformat())
    ]
    cursor.executemany("""
    INSERT INTO messages (order_id, sender_role, sender_name, original_text, translated_text, detected_language, target_language, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, messages)

    # 11. Demand Forecasts
    forecasts = [
        ("Paithani Handloom", "Maharashtra", 28.5, 6,
         json.dumps(["Upcoming Gudi Padwa & Wedding Season", "34% spike in ONDC search terms for 'Pure Silk Paithani'"]),
         json.dumps(["Gudi Padwa (April)", "Akshaya Tritiya (May)"]), now),
        ("Madhubani Folk Painting", "Bihar", 18.2, 4,
         json.dumps(["Rise in demand for sustainable eco-friendly wall art", "Corporate Diwali gifting inquiries"]),
         json.dumps(["Chhath Puja", "Diwali"]), now),
        ("Jaipur Blue Pottery", "Rajasthan", 22.0, 8,
         json.dumps(["Urban home decor trends favor lead-free pottery", "High repeat buyer retention"]),
         json.dumps(["Teej Festival", "Navratri"]), now),
        ("Kanchipuram Silk Saree", "Tamil Nadu", 31.0, 5,
         json.dumps(["South Indian Wedding season demand surge", "High demand for authentic Korvai temple border"]),
         json.dumps(["Pongal", "Chithirai Festival"]), now)
    ]
    cursor.executemany("""
    INSERT INTO demand_forecasts (craft_category, region, expected_demand_growth_pct, suggested_extra_units, reasons, upcoming_festivals, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, forecasts)

    conn.commit()
    conn.close()
