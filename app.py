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


@app.route("/frequencies", methods=["GET"])
def get_frequencies():
    my_texts, other_texts = scraper.all_messages(write_to_db=False)
    my_analyzer = MessageAnalyzer(my_texts)
    other_analyzer = MessageAnalyzer(other_texts)
    my_freqs = my_analyzer.word_cloud(False)
    other_freqs = other_analyzer.word_cloud(False)
    return jsonify({TARGETS[0]: my_freqs, TARGETS[1]:other_freqs})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port, threaded=True)
    app.run(debug=True)