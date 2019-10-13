from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

correct_years = ["2013", "1919", "1957", "1998", "1971", "1971", "1936"]

@app.route("/check")
def check_solution():
    solution_data = request.json()
    return jsonify(solution_data)


@app.route("/")
def index():
    return render_template("main.html",
                           years=random.sample(correct_years,
                                               len(correct_years)))

