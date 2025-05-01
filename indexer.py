import os
import re
import json

def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def build_index(pages_dir="data/pages", books_dir="data/books"):
    index = {}
    sentence_map = {}

    def process_file(filepath, filename_prefix):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
            sentences = split_sentences(raw_text)

            for sentence in sentences:
                sentence_id = f"{filename_prefix}::{sentence[:50]}"
                sentence_map[sentence_id] = sentence.strip()

                for word in set(tokenize(sentence)):
                    index.setdefault(word, []).append(sentence_id)

    # Process crawled web pages
    for filename in os.listdir(pages_dir):
        process_file(os.path.join(pages_dir, filename), filename)

    # Process books
    for filename in os.listdir(books_dir):
        process_file(os.path.join(books_dir, filename), filename)

    # Save
    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    with open("sentences.json", "w", encoding="utf-8") as f:
        json.dump(sentence_map, f, indent=2)

if __name__ == "__main__":
    build_index()
