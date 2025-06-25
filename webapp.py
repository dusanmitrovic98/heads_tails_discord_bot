from flask import Flask, render_template, jsonify, send_from_directory
import random
import os

app = Flask(__name__)

GIF_PATHS = {
    "heads": "heads.gif",
    "tails": "tails.gif"
}

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
