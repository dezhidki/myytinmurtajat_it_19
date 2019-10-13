from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import app_state
from flask import Flask, render_template, jsonify, redirect, url_for, session, request
import time
import binascii
import os
import functools
from admin import admin
from extra_challenge import challenge

app = Flask(__name__)
app.register_blueprint(admin)
app.secret_key = os.getenv("SESSION_KEY").encode()

KOODI_VERIFICATION = os.getenv("KOODI_VERIFICATION")


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def group_bits(text):
    return " ".join(text[i:i + 4] for i in range(0, len(text), 4))


def verify_solution(view):
    @functools.wraps(view)
    def decorator(**kwargs):
        if "password" in session:
            if session["password"] != app_state.current_password:
                session.clear()
                return redirect(url_for("index"))
        else:
            return redirect(url_for("index"))
        return view(**kwargs)
    return decorator


@app.route("/final_letters/<string:token>")
def get_final_letters(token):
    if token != KOODI_VERIFICATION:
        return jsonify({
            "ok": False
        })

    return jsonify({
        "ok": True,
        "fifth": app_state.current_password[4],
        "sixth": app_state.current_password[5]
    })


@app.route("/skip_news")
def check_news_state():
    if not app_state.skip_news:
        return jsonify({
            "skip": False
        })

    app_state.skip_news = False
    return jsonify({
        "skip": True,
        "fifth": app_state.current_password[4],
        "sixth": app_state.current_password[5]
    })


@app.route("/extra_challenge")
@verify_solution
def extra_challenge():
    challenge.start()
    return "Extra challenge!"

@app.route("/victory")
@verify_solution
def solution():
    return render_template("win.html", win_url=app_state.current_win_url)


@app.route("/verify/<string:code>", methods=["GET"])
def check_solution(code):
    if code != app_state.current_password:
        session.clear()
        return jsonify({
            "success": False,
            "redirect": None
        })

    session["password"] = code
    session["redirect_location"] = "solution"

    if challenge.enabled and app_state.play_extra_challenge:
        session["redirect_location"] = "extra_challenge"

    return jsonify({
        "success": True,
        "redirect": url_for(session["redirect_location"])
    })


@app.route("/")
def index():
    if "password" in session:
        if session["password"] == app_state.current_password:
            return redirect(url_for(session["redirect_location"]))
        else:
            session.clear()
    first_letter = group_bits(text_to_bits(app_state.current_password[0]))
    second_letter = group_bits(text_to_bits(app_state.current_password[1]))
    return render_template("koodi_main.html", first_letter=first_letter, second_letter=second_letter)
