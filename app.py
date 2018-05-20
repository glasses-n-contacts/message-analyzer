import os
from flask import Flask, render_template, send_from_directory, jsonify, request, redirect,url_for
from analyzer import MessageAnalyzer
from scraper import MessageScraper
from variables import *

app = Flask(__name__)

scraper = MessageScraper(ABSOLUTE_PATH, CONTACT_INFO, NAME)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/all_texts", methods=["GET"])
def all_texts():
    my_texts, other_texts = scraper.all_messages()
    return jsonify(my_texts + other_texts)


@app.route("/data")
def get_data():
    my_texts, other_texts = scraper.all_messages()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port, threaded=True)
    app.run(debug=True)