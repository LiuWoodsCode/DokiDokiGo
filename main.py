from flask import Flask, render_template, request

from ddgs import DDGS


app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")


@app.get("/search")
def search():
    query = request.args.get("q", "")
    page_str = request.args.get("pg", "1") # ddgs defaults to 1
    page = int(page_str)
    results = []
    if query:
        try:
            results = DDGS().text(query, max_results=10, page=page)
        except Exception as exc:
            # This should probably be a seperate page but for now just do it like this
            results = [{"title": "Search error", "href": "#", "body": str(exc)}]

    return render_template("search.html", query=query, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
