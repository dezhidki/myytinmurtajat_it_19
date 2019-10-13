from flask import Flask, render_template, request, jsonify
import random
import requests
import os
import urllib.parse
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)

correct_years = ["2013", "1919", "1957", "1998", "1971", "1971", "1936"]

KOODI_ADDRESS = os.getenv("KOODI_ADDRESS")
KOODI_VERIFICATION = os.getenv("KOODI_VERIFICATION")

@app.route("/poll")
def poll_skip():
    skip_news_req = requests.get(
        f"{KOODI_ADDRESS}/skip_news")
    skip_news = skip_news_req.json()

    if skip_news_req.status_code != 200 or not skip_news["skip"]:
        return jsonify({
            "skip": False
        })

    return jsonify({
        "skip": True,
        "renderContent": render_template("solution_comment.html",
                                         solution_fifth_char=skip_news["fifth"],
                                         solution_sixth_char=skip_news["sixth"])
    })

@app.route("/check", methods=["POST"])
def check_solution():
    solution_data = request.json

    if solution_data["solutions"] != correct_years:
        return jsonify({
            "correct": False,
            "renderContent": None
        })

    final_letters_res = requests.get(
        f"{KOODI_ADDRESS}/final_letters/{urllib.parse.quote(KOODI_VERIFICATION)}")
    final_letters = final_letters_res.json()

    if final_letters_res.status_code != 200 or not final_letters["ok"]:
        return jsonify({
            "correct": False,
            "renderContent": None
        })

    return jsonify({
        "correct": True,
        "renderContent": render_template("solution_comment.html",
                                         solution_fifth_char=final_letters["fifth"],
                                         solution_sixth_char=final_letters["sixth"])
    })


@app.route("/")
def index():
    return render_template("main.html",
                           years=random.sample(correct_years,
                                               len(correct_years)))
