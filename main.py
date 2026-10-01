from flask import Flask, render_template_string, request

from ddgs import DDGS


app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ query or "Search" }}</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px auto;
            padding: 0 20px;
        }

        form {
            margin-bottom: 35px;
        }

        input {
            width: 70%;
            padding: 12px;
            font-size: 16px;
        }

        button {
            padding: 12px 20px;
            font-size: 16px;
        }

        .result {
            margin-bottom: 28px;
        }

        .title {
            font-size: 20px;
            color: #1a0dab;
            text-decoration: none;
        }

        .title:hover {
            text-decoration: underline;
        }

        .url {
            color: #188038;
            font-size: 14px;
            margin: 4px 0;
        }

        .description {
            line-height: 1.4;
        }
    </style>
</head>

<body>

    <form action="/search" method="GET">
        <input
            name="q"
            value="{{ query }}"
            placeholder="Search..."
            autofocus
        >
        <button type="submit">Search</button>
    </form>

    {% for result in results %}
    <div class="result">
        <a class="title" href="{{ result.href }}">{{ result.title }}</a>
        <div class="url">{{ result.href }}</div>
        <div class="description">{{ result.body }}</div>
    </div>
    {% endfor %}

</body>
</html>
"""


@app.get("/")
@app.get("/search")
def search():
    query = request.args.get("q", "")
    results = []
    if query:
        try:
            results = DDGS().text(query, max_results=10)
        except Exception as exc:
            results = [{"title": "Search error", "href": "#", "body": str(exc)}]

    return render_template_string(PAGE, query=query, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
