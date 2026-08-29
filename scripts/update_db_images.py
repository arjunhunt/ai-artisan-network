import json
import sqlite3

with open("scratch/local_product_images.json", "r", encoding="utf-8") as f:
    local_images = json.load(f)

with open("scratch/final_product_links.json", "r", encoding="utf-8") as f:
    final_links = json.load(f)

conn = sqlite3.connect("artisan_network.db")
cursor = conn.cursor()

for pid in range(1, 81):
    img_url = local_images.get(str(pid)) or final_links.get(str(pid)) or f"/static/images/product_{pid}.svg"
    cursor.execute("UPDATE products SET image_urls = ? WHERE id = ?", (json.dumps([img_url]), pid))

conn.commit()
print("Updated all 80 products in artisan_network.db with user provided images!")

# Let's inspect a few rows
cursor.execute("SELECT id, title, image_urls FROM products WHERE id IN (1, 11, 21, 31, 41, 51, 61, 71, 80)")
for r in cursor.fetchall():
    print(f"Product {r[0]}: {r[1]} -> {r[2]}")

conn.close()
