import json
import re

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def load_index():
    with open("index.json", "r", encoding="utf-8") as f:
        index = json.load(f)
    with open("sentences.json", "r", encoding="utf-8") as f:
        sentence_map = json.load(f)
    with open("url_map.json", "r", encoding="utf-8") as f:
        url_map = json.load(f)
    return index, sentence_map, url_map

def search(query, index, sentence_map, url_map):
    query_words = tokenize(query)
    hit_counts = {}

    for word in query_words:
        if word in index:
            for sid in index[word]:
                hit_counts[sid] = hit_counts.get(sid, 0) + 1

    # Rank sentences by # of matching query words
    sorted_hits = sorted(hit_counts.items(), key=lambda x: x[1], reverse=True)
    results = []

    for sid, score in sorted_hits[:10]:  # top 10 results
        filename, _ = sid.split("::", 1)
        url = url_map.get(filename, "#")
        sentence = sentence_map[sid]

        # Boost score if sentence has relevant context words
        if any(kw in sentence.lower() for kw in ["founded", "established", "created", "launched", "invented"]):
            score += 1
        if re.search(r"\b(18|19|20)\d{2}\b", sentence):  # contains a year
            score += 1

        results.append((url, sentence.strip()))

    return results


# TEST