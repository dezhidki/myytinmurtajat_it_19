from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

correct_years = ["2013", "1919", "1957", "1998", "1971", "1971", "1936"]


@app.route("/check", methods=["POST"])
def check_solution():
    solution_data = request.json

    if solution_data["solutions"] != correct_years:
        return jsonify({
            "correct": False,
            "renderContent": None
        })

    return jsonify({
        "correct": True,
        "renderContent": render_template("solution_comment.html",
                                         solution_fifth_char="A",
                                         solution_sixth_char="B")
    })


@app.route("/")
def index():
    return render_template("main.html",
                           years=random.sample(correct_years,
                                               len(correct_years)))
