import os
import requests
from bs4 import BeautifulSoup
import time
import random
import json
from urllib.parse import urljoin, urlparse

DATA_DIR = "data/pages"
os.makedirs(DATA_DIR, exist_ok=True)
url_map = {}

def save_page(url, content):
    safe_name = url.replace("/", "_").replace(":", "").replace("?", "_")
    filename = safe_name + ".txt"
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    url_map[filename] = url

def sloth_bot(seed_url, max_pages=10):
    urls = [seed_url]
    visited = set()

    while urls and len(visited) < max_pages:
        url = urls.pop(0)
        if url in visited:
            continue

        print("Crawling:", url)
        time.sleep(random.uniform(1, 2))

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        save_page(url, soup.get_text())
        visited.add(url)

        for tag in soup.select("a[href]"):
            href = tag["href"]
            if href.startswith("/wiki") and ":" not in href:
                full_url = urljoin(seed_url, href)
                if full_url not in visited:
                    urls.append(full_url)

    with open("url_map.json", "w", encoding="utf-8") as f:
        json.dump(url_map, f, indent=2)

if __name__ == "__main__":
    sloth_bot("https://en.wikipedia.org/wiki/Google", max_pages=20)
