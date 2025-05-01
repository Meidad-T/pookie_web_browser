import os
import re
import json

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def build_index(data_dir="data/pages"):
    index = {}
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            words = set(tokenize(f.read()))
            for word in words:
                index.setdefault(word, []).append(filename)

    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

if __name__ == "__main__":
    build_index()
