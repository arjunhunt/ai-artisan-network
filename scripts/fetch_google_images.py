import urllib.request
import urllib.parse
import re
import json

queries = [
    ("paithani", "Paithani silk saree handwoven"),
    ("madhubani", "Madhubani painting Mithila art handmade"),
    ("blue_pottery", "Jaipur blue pottery handmade ceramic vase"),
    ("dhokra", "Dhokra brass bell metal tribal handicraft"),
    ("kanchipuram", "Kanchipuram silk saree pure zari"),
    ("bamboo", "Assam bamboo cane handmade basket craft"),
    ("kantha", "Kantha stitch embroidery silk dupatta saree"),
    ("pashmina", "Kashmir pashmina cashmere shawl handmade")
]

results = {}

for key, q in queries:
    url = f"https://www.google.com/search?q={urllib.parse.quote(q)}&tbm=isch&udm=2"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            # Find encrypted-tbn0.gstatic.com URLs
            found = re.findall(r'https://encrypted-tbn0\.gstatic\.com/images\?q=[^"\'<>\s&]+', body)
            # clean up
            cleaned = []
            seen = set()
            for f in found:
                # remove trailing backslashes or encoding issues
                clean = f.split("\\")[0]
                if clean not in seen and len(clean) > 30:
                    seen.add(clean)
                    cleaned.append(clean)
            results[key] = cleaned
            print(f"Key {key}: Found {len(cleaned)} Google image links")
    except Exception as e:
        print(f"Error {key}: {e}")

with open("google_image_links.json", "w") as out:
    json.dump(results, out, indent=2)
print("Saved to google_image_links.json")
