import os
import re
import json

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def build_index(data_dir="data/pages"):
    index = {}
    sentence_map = {}

    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()
            sentences = split_sentences(raw_text)

            for sentence in sentences:
                sentence_id = f"{filename}::{sentence[:50]}"  # unique-ish ID
                sentence_map[sentence_id] = sentence.strip()

                words = set(tokenize(sentence))
                for word in words:
                    index.setdefault(word, []).append(sentence_id)

    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    with open("sentences.json", "w", encoding="utf-8") as f:
        json.dump(sentence_map, f, indent=2)

if __name__ == "__main__":
    build_index()
