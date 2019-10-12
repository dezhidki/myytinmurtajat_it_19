from flask import Flask, render_template, jsonify, redirect, url_for, session
import time
import binascii
import os
import functools

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY").encode()

current_password = "TEST2"


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def group_bits(text):
    return " ".join(text[i:i + 4] for i in range(0, len(text), 4))


def verify_solution(view):
    @functools.wraps(view)
    def decorator(**kwargs):
        if "password" in session:
            if session["password"] != current_password:
                session.clear()
                return redirect(url_for("index"))
        else:
            return redirect(url_for("index"))
        return view(**kwargs)
    return decorator


@app.route("/victory")
@verify_solution
def solution():
    return "Solution"


@app.route("/verify/<string:code>", methods=["GET"])
def check_solution(code):
    if code != current_password:
        session.clear()
        return jsonify({
            "success": False,
            "redirect": None
        })

    session["password"] = code
    session["redirect_location"] = "solution"
    return jsonify({
        "success": True,
        "redirect": url_for(session["redirect_location"])
    })


@app.route("/")
def index():
    if "password" in session:
        if session["password"] == current_password:
            return redirect(url_for(session["redirect_location"]))
        else:
            session.clear()
    first_letter = group_bits(text_to_bits(current_password[0]))
    second_letter = group_bits(text_to_bits(current_password[1]))
    return render_template("koodi_main.html", first_letter=first_letter, second_letter=second_letter)
