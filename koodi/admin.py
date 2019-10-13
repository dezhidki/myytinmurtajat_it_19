from flask import Blueprint, render_template, request, Response, session, redirect, url_for
import app_state
import functools
import os
from extra_challenge import challenge as ex_challege

admin = Blueprint("admin", __name__, url_prefix="/admin")

USER = os.getenv("ADMIN_AUTH_USERNAME")
PASS = os.getenv("ADMIN_AUTH_PASSWORD")


def authenticate():
    auth = request.authorization
    if auth and auth.type == "basic" and auth.username == USER and auth.password == PASS:
        return True
    return False


def challenge():
    return Response(
        status=401,
        headers={
            "WWW-Authenticate": "Basic realm=''"
        }
    )


def check_auth(view):
    @functools.wraps(view)
    def decorator(*args, **kwargs):
        if authenticate():
            return view(*args, **kwargs)
        else:
            return challenge()
    return decorator


@admin.route("/")
@check_auth
def index():
    return render_template("admin.html",
                           current_password=app_state.current_password,
                           current_win_url=app_state.current_win_url,
                           current_skip_year_puzzle=app_state.skip_news,
                           enable_extra_challenge=ex_challege.enabled,
                           current_enable_extra_challenge=app_state.play_extra_challenge,
                           current_in_challenge=app_state.in_challenge)


@admin.route("/update_pass", methods=["POST"])
@check_auth
def update_pass():
    app_state.current_password = request.form["new_pass"].upper()
    return redirect(url_for("admin.index"))


@admin.route("/update_url", methods=["POST"])
@check_auth
def update_url():
    app_state.current_win_url = request.form["new_url"]
    return redirect(url_for("admin.index"))


@admin.route("/solve_year_puzzle", methods=["POST"])
@check_auth
def solve_year_puzzle():
    app_state.skip_news = True
    return redirect(url_for("admin.index"))

@admin.route("/stop_extra_challenge", methods=["POST"])
@check_auth
def stop_extra_challenge():
    ex_challege.stop()
    app_state.in_challenge = False

@admin.route("/enable_extra_challenge", methods=["POST"])
@check_auth
def enable_extra_challenge():
    app_state.play_extra_challenge = True
    return redirect(url_for("admin.index"))
