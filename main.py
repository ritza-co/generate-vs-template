from flask import Flask, render_template, request, jsonify
from get_headings import get_top_comparisons
import os
import json


app = Flask(__name__)

@app.route("/")
def main():
    seed = request.args.get('seed', 'venture capital')
    seed = seed.lower()
    if not seed:
        return render_template("index.html", seed=seed)
    else:
        print("here")
        title, headings = get_top_comparisons(seed)
        print(headings)
        return render_template("index.html", title=title, headings=headings, seed=seed)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run("0.0.0.0")