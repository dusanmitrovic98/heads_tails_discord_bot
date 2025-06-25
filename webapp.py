from flask import Flask, render_template, jsonify, send_from_directory
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GIF_PATHS = {
    "heads": "heads.gif",
    "tails": "tails.gif"
}

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
