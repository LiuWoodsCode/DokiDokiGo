from flask import Flask, render_template, request

from ddgs import DDGS


app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")


@app.get("/search")
def search():
    query = request.args.get("q", "")
    results = []
    if query:
        try:
            results = DDGS().text(query, max_results=10)
        except Exception as exc:
            results = [{"title": "Search error", "href": "#", "body": str(exc)}]

    return render_template("search.html", query=query, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
