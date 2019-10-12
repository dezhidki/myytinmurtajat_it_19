from flask import Blueprint, render_template, request, Response, session, redirect, url_for
import app_state
from flask_basicauth import BasicAuth
import functools
import os

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
    return render_template("admin.html", current_password=app_state.current_password, current_win_url=app_state.current_win_url)


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
