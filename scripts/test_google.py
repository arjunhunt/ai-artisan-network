import urllib.request
import re

url = "https://www.google.com/search?q=paithani+saree&udm=2"
req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req, timeout=10) as resp:
    data = resp.read().decode("latin-1", errors="ignore")
    # find all http links
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
    print("Found total links:", len(links))
    for l in links[:15]:
        print(l)
