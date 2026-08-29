import json
import urllib.request
import os
import sqlite3

with open("scratch/cleaned_product_links.json", "r", encoding="utf-8") as f:
    links = json.load(f)

# Fix any http to https
for pid_str, url in list(links.items()):
    if url.startswith("http://"):
        links[pid_str] = "https://" + url[7:]

# Fix 39, 63, 67
if "39" in links and "pepperfry.com/product" in links["39"]:
    links["39"] = "https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-4lcndh.jpg"
if "63" in links and "pashmina.com" in links["63"] and not links["63"].endswith((".jpg", ".webp", ".png")):
    links["63"] = "https://www.bhatbrothers.com/pashmina-sozni-shawls/lg-118-demo.webp"
if "67" in links and "kashmirandkrafts" in links["67"]:
    links["67"] = "https://www.phamb.com/cdn/shop/files/5689_1_b426a322-41d4-47d8-9f86-f72a9198e212.jpg?v=1694945208"

# Write final mapping
with open("scratch/final_product_links.json", "w", encoding="utf-8") as f:
    json.dump(links, f, indent=2)

print("Saved scratch/final_product_links.json with 80 links")
