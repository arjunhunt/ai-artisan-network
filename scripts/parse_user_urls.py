import re
import urllib.request
import os
import json
import sqlite3

raw_text = """
https://www.karagiri.com/cdn/shop/files/DEEPMALA-BWDEE-1003-1.jpg?v=1705574077
https://onlypaithani.com/cdn/shop/files/MBPBUAB0214_a7813c9a-bdf1-4326-a3fb-866035ebbd4d_1800x1800.jpg?v=1755434705
https://kaathpadar.com/cdn/shop/files/paithanisilksaree.jpg?v=1752064590&width=1946
https://www.luxurionworld.com/cdn/shop/files/ID1P1PR525040902_Blue_Paithani_Handloom_Pure_Silk_Muniya_Border_Bird_Design_Dupatta.jpg?v=1744706555&width=3840
https://www.luxurionworld.com/cdn/shop/files/ID1P1PR525040902_Blue_Paithani_Handloom_Pure_Silk_Muniya_Border_Bird_Design_Dupatta_1.jpg?v=1744706555&width=3840
https://www.luxurionworld.com/cdn/shop/files/ID1P1PR525040902_Blue_Paithani_Handloom_Pure_Silk_Muniya_Border_Bird_Design_Dupatta_2.jpg?v=1744706555&width=3840
https://www.luxurionworld.com/cdn/shop/files/ID1P1PR525040902_Blue_Paithani_Handloom_Pure_Silk_Muniya_Border_Dupatta_1.jpg?v=1744706555&width=3840
https://www.luxurionworld.com/cdn/shop/files/ID1P1PR525040902_Blue_Paithani_Handloom_Pure_Silk_Muniya_Border_Dupatta_2.jpg?v=1744706555&width=3840
https://www.luxurionworld.com/cdn/shop/files/ID1P1PR525040902_Blue_Paithani_Handloom_Pure_Silk_Muniya_Border_Dupatta_3.jpg?v=1744706555&width=3840
https://www.luxurionworld.com/cdn/shop/files/ID1P1PR525040902_Blue_Paithani_Handloom_Pure_Silk_Muniya_Border_Dupatta_4.jpg?v=1744706555&width=3840
https://cdn.exoticindia.com/images/products/original/madhuban/di28.jpg
https://cdn.exoticindia.com/images/products/original/madhuban/kohbar__auspicious_marriage_diagram_dd95.jpg
https://borderlessjournal.com/wp-content/uploads/2023/11/wedding-procession.jpg
https://www.silkrute.co.uk/images/detailed/723/72672.001.jpg
https://indianfolkart.org/wp-content/uploads/2021/08/Madhubani-Anjali-09.jpg
https://i.etsystatic.com/43391614/r/il/0eb2e0/5692613071/il_794xN.5692613071_o3rd.jpg
https://media.assettype.com/deccanherald%2Fimport%2Fsites%2Fdh%2Ffiles%2Farticle_images%2F2020%2F05%2F19%2Ffile7735anv5sb71jyvwhf6f-2099006174-1569094201.jpg?auto=format%2Ccompress&fit=max&w=undefined
https://cdn.exoticindia.com/images/products/original/artimages/madhubani-painting1.webp
https://cdn.exoticindia.com/images/products/original/artimages/madhubani-painting3.webp
https://www.exoticindiaart.com/product/paintings/matsya-avatara-first-incarnation-of-lord-vishnu-madhubani-painting-miy029/
https://cdn.shopify.com/s/files/1/0617/9209/2220/files/Blue_Pottery_Flower_Vase_18.jpg?v=1757133993
https://cdn.vibecity.in/providers/61dc119f7864df0011da13c3/13ed9ac8-4a74-4e8f-8966-e0baff65939c_dc64f2b2-d9e1-4eed-a676-b91ebe77e32c.png
https://www.neerjainternational.com/sites/default/files/NBPWP-8011-FRONT.jpg
https://www.arraish.com/cdn/shop/files/F789520E-40A4-4FD7-A5D9-E7B27EF609A1.jpg?v=1762859243&width=533
https://www.arraish.com/cdn/shop/files/80420AAD-058C-4746-A0AA-9D9646F179DC.jpg?v=1735285138&width=533
https://www.arraish.com/cdn/shop/products/mugs-drinkware-tranquility-mug-with-lid-28410683752530.png?v=1633779494&width=533
https://www.arraish.com/cdn/shop/files/6066FA87-7855-4DFF-BDCE-DFB74BDADCAF.jpg?v=1784355718&width=533
https://www.organizeit.com/cdn/shop/products/alt_bamboo-office-organizer_1_1080x.jpg?v=1679559205
https://www.mystore.in/s/62ea2c599d1398fa16dbae0a/66a74baf5a4a4302bb925f50/whatsapp_image_2024-07-26_at_1-37-38_pm-removebg-preview.png
https://cdn.webshopapp.com/shops/281984/files/274738495/1200x1200x2/brot-servierkorb-natur.jpg
https://i5.walmartimages.com/seo/Sowpeace-Dhokra-Deer-Brass-Artisan-Figurine-Tabletop-Decor_e1ecdf5c-85f3-4e18-9a55-f9ca356306fc.acd0dcf6a1f3da87e1c6bdc5ea442c18.jpeg?odnBg=FFFFFF&odnHeight=117&odnWidth=117
https://i5.walmartimages.com/asr/59c17504-2c5d-426e-b39c-939a8e57a573.988368f0682adefbc46020139a689561.jpeg?odnBg=FFFFFF&odnHeight=117&odnWidth=117
https://i5.walmartimages.com/asr/e3f12fee-aab3-49f1-bf5a-92c07df6a910.b4d3b52cba850a56789d6d5e8efc5961.jpeg?odnBg=FFFFFF&odnHeight=117&odnWidth=117
https://i5.walmartimages.com/asr/7da59dbb-913b-44d0-9614-333de39a68fd.730178a1df4f7cf43eb39426089d5110.jpeg?odnBg=FFFFFF&odnHeight=117&odnWidth=117
https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-4lcndh.jpg
https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-dbxk1m.jpg
https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-yopuoa.jpg
https://ii1.pepperfry.com/media/catalog/product/b/r/90x99/brass-dhokra-crafted-horse-with-rider-tribal-handicraft-bastar-art-by-coshal-arts-brass-dhokra-craft-ln3f4c.jpg
https://www.pepperfry.com/product/dancing-figurine-set-dhokra-art-2300600.html
https://www.advaitahandicrafts.com/products/nandi-bull-in-dhokra-art-form-handcrafted-dhokra-art-brass
https://cliosilks.com/cdn/shop/files/DSC05153.jpg?v=1700941374&width=1080
https://cliosilks.com/cdn/shop/files/DSC05172_02368ca1-741e-4518-9a5a-d2d251120fde.jpg?v=1700941362&width=1080
https://cliosilks.com/cdn/shop/files/DSC05145_b63a46d2-24c5-49bc-9810-23e1901b60b8.jpg?v=1700941362&width=1080
https://cliosilks.com/cdn/shop/files/DSC05179.jpg?v=1700941361&width=1080
https://cliosilks.com/cdn/shop/files/DSC05174.jpg?v=1700941361&width=1080
https://cliosilks.com/cdn/shop/files/DSC05143_f0b362ee-be30-4fa1-a0e9-09428da3ae5e.jpg?v=1700941361&width=1080
https://cliosilks.com/cdn/shop/files/DSC05150.jpg?v=1700941361&width=1080
https://cliosilks.com/cdn/shop/files/DSC05163.jpg?v=1700941361&width=1080
https://cliosilks.com/cdn/shop/files/DSC09769_6194ef1b-3dad-489e-bf37-4fcb9126dd1f.jpg?v=1738584098
https://cliosilks.com/cdn/shop/files/DSC03672_6535eda9-2d61-430e-87cd-cb5379553653.jpg?v=1730812531
https://www.organizeit.com/cdn/shop/products/alt_bamboo-office-organizer_1_1080x.jpg?v=1679559205
https://www.mystore.in/s/62ea2c599d1398fa16dbae0a/66a74baf5a4a4302bb925f50/whatsapp_image_2024-07-26_at_1-37-38_pm-removebg-preview.png
https://cdn.webshopapp.com/shops/281984/files/274738495/1200x1200x2/brot-servierkorb-natur.jpg
https://punarnawa.com/cdn/shop/files/punarnawa-soul-of-artistry-fruit-basket-default-title-bamboo-trivet-fruit-stand-32440699682873.jpg?v=1705108848
https://cdn.produceshop.com/184119-large_default/cesto-porta-biancheria-rettangolare-da-bagno-bamb-federa-beige-zahara.jpg
https://www.organizeit.com/cdn/shop/products/alt_bamboo-office-organizer_1_1080x.jpg?v=1679559205
https://punarnawa.com/cdn/shop/files/punarnawa-soul-of-artistry-fruit-basket-default-title-bamboo-trivet-fruit-stand-32440699682873.jpg?v=1705108848
https://cdn.webshopapp.com/shops/281984/files/274738495/1200x1200x2/brot-servierkorb-natur.jpg
https://cdn.produceshop.com/184119-large_default/cesto-porta-biancheria-rettangolare-da-bagno-bamb-federa-beige-zahara.jpg
https://www.organizeit.com/cdn/shop/products/alt_bamboo-office-organizer_1_1080x.jpg?v=1679559205
https://www.bhatbrothers.com/pashmina-sozni-shawls/lg-118-demo.webp
https://www.phamb.com/products/black-pashmina-shawl-with-tilla-embroidery-5689
https://www.pashmina.com/tanisha-emerald-kani-shawl/
https://www.exoticindiaart.com/product/textiles/true-red-pure-pashmina-shawl-with-sozni-embroidered-paisley-jaal-gaf305/
https://www.artasia.shop/products/white-chinar-pashmina-shawl
https://www.exoticindiaart.com/product/textiles/dark-purple-pure-pashmina-shawl-with-large-sozni-embroidered-chinar-leaves-shr86/
https://www.kashmirandkrafts.com/products/tbc19
https://www.kashmirorigin.com/products/leaf-green-sozni-embroidered-handwoven-pashmina-shawl
https://www.treasuresofkashmir.in/products/black-golden-chinar-ladies-hand-embroidered-cashmere-pashmina-shawl
https://kepra.in/products/black-pashmina-jaldaar-chinar-embroidery-sozni-stole
https://www.arraish.com/cdn/shop/files/F789520E-40A4-4FD7-A5D9-E7B27EF609A1.jpg?v=1762859243&width=533
https://www.arraish.com/cdn/shop/files/80420AAD-058C-4746-A0AA-9D9646F179DC.jpg?v=1735285138&width=533
https://www.arraish.com/cdn/shop/products/mugs-drinkware-tranquility-mug-with-lid-28410683752530.png?v=1633779494&width=533
https://www.arraish.com/cdn/shop/files/6066FA87-7855-4DFF-BDCE-DFB74BDADCAF.jpg?v=1784355718&width=533
https://cdn.shopify.com/s/files/1/0617/9209/2220/files/Blue_Pottery_Flower_Vase_18.jpg?v=1757133993
https://cdn.vibecity.in/providers/61dc119f7864df0011da13c3/13ed9ac8-4a74-4e8f-8966-e0baff65939c_dc64f2b2-d9e1-4eed-a676-b91ebe77e32c.png
https://www.neerjainternational.com/sites/default/files/NBPWP-8011-FRONT.jpg
https://cdn.exoticindia.com/images/products/original/madhuban/di28.jpg
https://borderlessjournal.com/wp-content/uploads/2023/11/wedding-procession.jpg
https://www.silkrute.co.uk/images/detailed/723/72672.001.jpg
"""

urls = [line.strip() for line in raw_text.strip().splitlines() if line.strip().startswith("http")]
print(f"Total URLs parsed: {len(urls)}")

# Let's create an exact mapping from 1 to 80
USER_PROVIDED_LINKS = {}
for i, url in enumerate(urls, 1):
    USER_PROVIDED_LINKS[i] = url

# Write JSON mapping to scratch
os.makedirs("scratch", exist_ok=True)
with open("scratch/user_product_links.json", "w", encoding="utf-8") as f:
    json.dump(USER_PROVIDED_LINKS, f, indent=2)

print("Saved scratch/user_product_links.json")
