import logging

from flask import Flask, abort, render_template, request

from ddgs import DDGS


app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.get("/")
def index():
    logger.debug("Rendering index page")
    return render_template("index.html")


@app.get("/search")
def search():
    query = request.args.get("q", "")
    page_str = request.args.get("pg", "1") # ddgs defaults to 1
    logger.info("Received search request (query length: %d)", len(query))
    try:
        page = int(page_str)
    except ValueError:
        logger.warning("Invalid page parameter")
        abort(400)

    if page < 1:
        logger.warning("Page parameter must be positive")
        abort(400)

    results = []
    if query:
        logger.debug("Starting search for page %d", page)
        try:
            results = DDGS().text(query, max_results=10, page=page)
            logger.info("Search completed with %d results", len(results))
        except Exception:
            # This should probably be a seperate page but for now just do it like this
            logger.exception("Search request failed")
            results = [{"title": "Search error", "href": "#", "body": "Please try again later."}]
    else:
        logger.debug("Skipping search because the query is empty")

    logger.debug("Rendering search page")
    return render_template("search.html", query=query, results=results)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.DEBUG)
    logger.info("Starting web server on 0.0.0.0:8050")
    app.run(host="0.0.0.0", port=8050)
