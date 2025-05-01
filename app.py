from flask import Flask, render_template, request
from search_engine import load_index, search

app = Flask(__name__)
index, sentence_map, url_map = load_index()

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        query = request.form["query"]
        results = search(query, index, sentence_map, url_map)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
