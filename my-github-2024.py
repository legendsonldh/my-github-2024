"""
This module provides a Flask application for GitHub data fetching and display.
"""

import json
import logging
import os
import threading

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy

from generator.context import get_context
from generator.fetch import fetch_github
from log.logging_config import setup_logging
from util import Github

setup_logging()

app = Flask(__name__)


def app_preparation():
    """
    Function to prepare the application.
    """
    app.secret_key = "my-github-2024"

    load_dotenv()
    app.config["CLIENT_ID"] = os.getenv("CLIENT_ID")
    app.config["CLIENT_SECRET"] = os.getenv("CLIENT_SECRET")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-github-2024.db"


app_preparation()


db = SQLAlchemy(app)


class RequestedUser(db.Model):
    """
    Model for requested GitHub users.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)


class UserContext(db.Model):
    """
    Model for storing user context data.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    context = db.Column(db.Text, nullable=False)


def db_preparation():
    """
    Function to prepare the database.
    """
    with app.app_context():
        db.create_all()
        missing_users = (
            db.session.query(RequestedUser)
            .outerjoin(UserContext, RequestedUser.username == UserContext.username)
            .filter(UserContext.username is None)
            .all()
        )
        for user in missing_users:
            logging.info("Missing user: %s", user.username)
            db.session.query(RequestedUser).filter_by(username=user.username).delete()
        db.session.commit()


db_preparation()


@app.before_request
def before_request():
    """
    Function to handle actions before each request.
    """
    if (
        request.endpoint not in ("status", "index", "login", "callback", "static")
        and "access_token" not in session
    ):
        return redirect(url_for("index"))

    if request.endpoint not in (
        "status",
        "index",
        "login",
        "callback",
        "dashboard",
        "load",
        "wait",
        "display",
        "static",
    ):
        return redirect(url_for("index"))

    return None


@app.route("/status", methods=["GET"])
def status():
    """
    Endpoint to check the status of the application.
    """
    return jsonify({"status": "ok"}), 200


@app.route("/", methods=["GET"])
def index():
    """
    Endpoint for the index page.
    """
    if session.get("access_token"):
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login", methods=["GET"])
def login():
    """
    Endpoint for the login page.
    """
    if session.get("access_token"):
        return redirect(url_for("dashboard"))
    github_authorize_url = "https://github.com/login/oauth/authorize"
    return redirect(
        f"{github_authorize_url}?client_id={app.config['CLIENT_ID']}&scope=repo,read:org"
    )


@app.route("/callback", methods=["GET"])
def callback():
    """
    Endpoint for the GitHub OAuth callback.
    """
    code = request.args.get("code")

    if not code:
        return redirect(url_for("index"))

    try:
        token_response = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": app.config["CLIENT_ID"],
                "client_secret": app.config["CLIENT_SECRET"],
                "code": code,
            },
            timeout=10,
        )
        token_json = token_response.json()
        access_token = token_json.get("access_token")
    except requests.exceptions.RequestException as e:
        logging.error("Error getting access token: %s", e)
        return redirect(url_for("index"))

    if not access_token:
        return redirect(url_for("index"))
    session["access_token"] = access_token
    return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Endpoint for the dashboard page.
    """
    access_token = session.get("access_token")
    headers = {"Authorization": f"bearer {access_token}"}
    logging.info("access_token: %s", access_token)
    user_response = requests.get(
        "https://api.github.com/user", headers=headers, timeout=10
    )
    user_data = user_response.json()

    username = user_data.get("login")
    session["username"] = username

    if UserContext.query.filter_by(username=username).first():
        return redirect(url_for("display"))
    if RequestedUser.query.filter_by(username=username).first():
        return redirect(url_for("wait"))
    return render_template("dashboard.html", user=user_data, access_token=access_token)


@app.route("/load", methods=["POST"])
def load():
    """
    Endpoint to load user data.
    """
    data = request.json

    access_token = data.get("access_token")
    username = data.get("username")
    timezone = data.get("timezone")
    year = int(data.get("year"))

    session["access_token"] = access_token
    session["username"] = username
    session["timezone"] = timezone
    session["year"] = year

    requested_user = RequestedUser(username=username)
    db.session.add(requested_user)
    db.session.commit()

    if not all([access_token, username, timezone, year]):
        return jsonify({"redirect_url": url_for("index", year=year)})

    def fetch_data():
        with app.app_context():
            github = Github(access_token, username, timezone)
            result_data, result_new_repo = fetch_github(github, year, skip_fetch=False)

            if result_data is None or result_new_repo is None:
                logging.error("Error fetching data from GitHub")
                return

            context = get_context(year, result_data, result_new_repo)

            user_context = UserContext(username=username, context=json.dumps(context))
            db.session.add(user_context)
            db.session.commit()

    fetch_thread = threading.Thread(target=fetch_data)
    fetch_thread.start()

    return jsonify({"redirect_url": url_for("wait")})


@app.route("/wait", methods=["GET"])
def wait():
    """
    Endpoint for the wait page.
    """
    username = session.get("username")
    if UserContext.query.filter_by(username=username).first():
        return redirect(url_for("display"))
    return render_template("wait.html")


@app.route("/display", methods=["GET"])
def display():
    """
    Endpoint for the display page.
    """
    username = session.get("username")
    user_context = UserContext.query.filter_by(username=username).first()
    if user_context:
        return render_template(
            "template.html", context=json.loads(user_context.context)
        )
    return redirect(url_for("wait"))


@app.route("/static/<path:filename>", methods=["GET"])
def static_files(filename):
    """
    Endpoint to serve static files.
    """
    return send_from_directory("static", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
