import json
import urllib.request
import re
import os

with open("scratch/user_product_links.json", "r", encoding="utf-8") as f:
    links = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

cleaned_links = {}

for pid_str, url in links.items():
    pid = int(pid_str)
    # If the URL is a html page (like pepperfry or pashmina product page), let's inspect or extract og:image
    if url.endswith(".html") or "/product/" in url or "/products/" in url:
        if not any(url.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=8) as resp:
                    html = resp.read().decode("utf-8", errors="ignore")
                    og_match = re.search(r'<meta property="og:image" content="([^"]+)"', html) or re.search(r'<meta name="og:image" content="([^"]+)"', html)
                    if og_match:
                        extracted = og_match.group(1)
                        if extracted.startswith("//"):
                            extracted = "https:" + extracted
                        print(f"Product {pid}: Extracted og:image from {url} -> {extracted}")
                        cleaned_links[pid] = extracted
                        continue
            except Exception as e:
                print(f"Product {pid}: Failed to scrape {url}: {e}")
    cleaned_links[pid] = url

with open("scratch/cleaned_product_links.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_links, f, indent=2)

print("Saved scratch/cleaned_product_links.json")
