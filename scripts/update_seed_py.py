import json

with open("scratch/local_product_images.json", "r", encoding="utf-8") as f:
    local_images = json.load(f)

with open("scratch/final_product_links.json", "r", encoding="utf-8") as f:
    final_links = json.load(f)

# Generate formatted python dictionary
entries = []
for pid in range(1, 81):
    img = local_images.get(str(pid)) or final_links.get(str(pid)) or f"/static/images/product_{pid}.svg"
    entries.append(f'    {pid}: "{img}"')

dict_code = "GOOGLE_IMAGE_LINKS = {\n" + ",\n".join(entries) + "\n}"

with open("backend/seed_data.py", "r", encoding="utf-8") as f:
    content = f.read()

import re
new_content = re.sub(r'GOOGLE_IMAGE_LINKS = \{[\s\S]*?\n\}', dict_code, content, count=1)

with open("backend/seed_data.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated GOOGLE_IMAGE_LINKS in backend/seed_data.py with user images!")
