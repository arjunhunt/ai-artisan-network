import urllib.request
import json

url = "https://en.wikipedia.org/w/api.php?action=query&titles=Paithani|Madhubani_art|Blue_Pottery_of_Jaipur|Dhokra|Kanchipuram_silk_sari|Kantha|Pashmina|Bamboo&prop=pageimages&format=json&pithumbsize=600"
req = urllib.request.Request(url, headers={"User-Agent": "SIHArtisanCommerce/1.0 (artisan@sih.gov.in)"})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    for pid, pdata in pages.items():
        title = pdata.get("title")
        thumb = pdata.get("thumbnail", {}).get("source")
        print(f"{title}: {thumb}")
