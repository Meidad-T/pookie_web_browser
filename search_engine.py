import json
import os
import re

def load_index():
    with open("index.json", "r", encoding="utf-8") as f:
        return json.load(f)

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def search(query, index, data_dir="data/pages"):
    with open("url_map.json", "r", encoding="utf-8") as f:
        url_map = json.load(f)

    keywords = tokenize(query)
    matched_files = set()

    for word in keywords:
        if word in index:
            matched_files.update(index[word])

    results = []
    for filename in matched_files:
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            preview_start = content.lower().find(keywords[0]) if keywords else 0
            preview = content[preview_start:preview_start + 300] if preview_start != -1 else content[:300]
            real_url = url_map.get(filename, "#")
            results.append((real_url, preview.strip()))

    return results
