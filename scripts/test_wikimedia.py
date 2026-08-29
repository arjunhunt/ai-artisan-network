import urllib.request
import urllib.parse
import json

def search_wikimedia_images(query, limit=10):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"file:{query}",
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url|mime|size|thumburl",
        "iiurlwidth": 800
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "SIHArtisanCommerce/1.0 (artisan@sih.gov.in)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            urls = []
            for pid, pdata in pages.items():
                infos = pdata.get("imageinfo", [])
                if infos:
                    thumb = infos[0].get("thumburl") or infos[0].get("url")
                    if thumb and any(thumb.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".jpg/800px-"]):
                        urls.append((pdata.get("title", ""), thumb))
            return urls
    except Exception as e:
        print("Error:", e)
        return []

print("Paithani:", search_wikimedia_images("Paithani saree", 5))
print("Madhubani:", search_wikimedia_images("Madhubani painting", 5))
print("Blue Pottery:", search_wikimedia_images("Jaipur Blue Pottery", 5))
print("Dhokra:", search_wikimedia_images("Dhokra", 5))
print("Kanchipuram:", search_wikimedia_images("Kanchipuram saree", 5))
print("Bamboo:", search_wikimedia_images("Bamboo basket India", 5))
print("Kantha:", search_wikimedia_images("Kantha embroidery", 5))
print("Pashmina:", search_wikimedia_images("Pashmina shawl", 5))
