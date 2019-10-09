from flask import Flask
import time


app = Flask(__name__)

@app.route("/")
def index():
    return f"Hello, world! Now is {time.clock()}"