from flask import Flask, render_template
import time


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("koodi_main.html")