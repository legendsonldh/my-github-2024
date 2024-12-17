from util import Github
from generator.fetch import fetch_github
from generator.context import get_context
from log.logging_config import setup_logging

from flask import (
    Flask,
    request,
    redirect,
    session,
    url_for,
    render_template,
    send_from_directory,
    jsonify,
)
import requests
from dotenv import load_dotenv
import os
import logging
import threading
from flask_sqlalchemy import SQLAlchemy
import json

setup_logging()

app = Flask(__name__)

secret_key = os.urandom(24)
app.secret_key = secret_key

load_dotenv()
app.config['CLIENT_ID'] = os.getenv("CLIENT_ID")
app.config['CLIENT_SECRET'] = os.getenv("CLIENT_SECRET")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-github-2024.db"
db = SQLAlchemy(app)


class RequestedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)


class UserContext(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    context = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.before_request
def before_request():
    if (
        request.endpoint not in ("index", "login", "callback", "static")
        and "access_token" not in session
    ):
        return redirect(url_for("index"))


@app.route("/", methods=["GET"])
def index():
    return render_template("login.html")


@app.route("/login")
def login():
    github_authorize_url = "https://github.com/login/oauth/authorize"
    return redirect(
        f"{github_authorize_url}?client_id={app.config['CLIENT_ID']}&scope=repo,read:org"
    )


@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],
            "code": code,
        },
    )
    token_json = token_response.json()
    access_token = token_json.get("access_token")
    session["access_token"] = access_token
    return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=["GET"])
def dashboard():
    access_token = session.get("access_token")
    headers = {"Authorization": f"bearer {access_token}"}
    logging.info(f"access_token: {access_token}")
    user_response = requests.get("https://api.github.com/user", headers=headers)
    user_data = user_response.json()

    username = user_data.get("login")

    user_context = UserContext.query.filter_by(username=username).first()
    if user_context:
        return render_template("template.html", context=json.loads(user_context.context))
    elif RequestedUser.query.filter_by(username=username).first():
        return render_template("wait.html")
    else:
        return render_template(
            "dashboard.html", user=user_data, access_token=access_token
        )


@app.route("/load", methods=["POST"])
def load():
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
    username = session.get("username")
    user_context = UserContext.query.filter_by(username=username).first()
    if user_context:
        return render_template(
            "template.html", context=json.loads(user_context.context)
        )
    else:
        return render_template("wait.html")


@app.route("/display", methods=["GET"])
def display():
    username = session.get("username")
    user_context = UserContext.query.filter_by(username=username).first()
    if user_context:
        return render_template(
            "template.html", context=json.loads(user_context.context)
        )
    else:
        return render_template("wait.html")


@app.route("/static/<path:filename>", methods=["GET"])
def static_files(filename):
    return send_from_directory("static", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
