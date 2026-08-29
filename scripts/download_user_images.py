import json
import urllib.request
import os

with open("scratch/final_product_links.json", "r", encoding="utf-8") as f:
    links = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

os.makedirs("frontend/images", exist_ok=True)
download_results = {}

for pid_str, url in links.items():
    pid = int(pid_str)
    dest_path = f"frontend/images/product_{pid}.jpg"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
            if len(content) > 500:  # Valid image payload
                with open(dest_path, "wb") as img_file:
                    img_file.write(content)
                download_results[pid] = f"/static/images/product_{pid}.jpg"
                print(f"[{pid}/80] Successfully downloaded {url[:60]}... ({len(content)} bytes)")
            else:
                download_results[pid] = url
                print(f"[{pid}/80] Small payload, keeping external URL")
    except Exception as e:
        download_results[pid] = url
        print(f"[{pid}/80] Fallback to URL (error: {e})")

with open("scratch/local_product_images.json", "w", encoding="utf-8") as f:
    json.dump(download_results, f, indent=2)

print("Finished processing all 80 images!")
