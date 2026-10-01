from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, quote_plus
from html import escape

from ddgs import DDGS


class SearchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        query = params.get("q", [""])[0]

        results = []
        if query:
            try:
                results = DDGS().text(query, max_results=10)
            except Exception as e:
                results = [{"title": "Search error", "href": "#", "body": str(e)}]

        result_html = ""

        for result in results:
            title = escape(result.get("title", ""))
            href = escape(result.get("href", ""))
            body = escape(result.get("body", ""))

            result_html += f"""
            <div class="result">
                <a class="title" href="{href}">{title}</a>
                <div class="url">{href}</div>
                <div class="description">{body}</div>
            </div>
            """

        page = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{escape(query) if query else "Search"}</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px auto;
            padding: 0 20px;
        }}

        form {{
            margin-bottom: 35px;
        }}

        input {{
            width: 70%;
            padding: 12px;
            font-size: 16px;
        }}

        button {{
            padding: 12px 20px;
            font-size: 16px;
        }}

        .result {{
            margin-bottom: 28px;
        }}

        .title {{
            font-size: 20px;
            color: #1a0dab;
            text-decoration: none;
        }}

        .title:hover {{
            text-decoration: underline;
        }}

        .url {{
            color: #188038;
            font-size: 14px;
            margin: 4px 0;
        }}

        .description {{
            line-height: 1.4;
        }}
    </style>
</head>

<body>

    <form action="/search" method="GET">
        <input
            name="q"
            value="{escape(query)}"
            placeholder="Search..."
            autofocus
        >
        <button type="submit">Search</button>
    </form>

    {result_html}

</body>
</html>
"""

        body = page.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", 8080), SearchHandler).serve_forever()