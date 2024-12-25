"""
This module provides a Flask application for GitHub data fetching and display.
"""

import json
import logging
import os
import threading

import requests
from dotenv import load_dotenv
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_sqlalchemy import SQLAlchemy

from log.logging_config import setup_logging
from util.context import get_context

setup_logging()

app = Flask(__name__)


def app_preparation():
    """
    Function to prepare the application.
    """
    app.secret_key = os.urandom(24)

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
    gitlab_authorize_url = "http://localhost:9999/oauth/authorize"
    redirect_uri = url_for('callback', _external=True)
    return redirect(
        f"{gitlab_authorize_url}?client_id={app.config['CLIENT_ID']}&response_type=code&redirect_uri={redirect_uri}&scope=read_user"
    )


@app.route("/callback", methods=["GET"])
def callback():
    """
    Endpoint for the GitLab OAuth callback.
    """
    logging.info("Callback received with args: %s", request.args)
    
    if "code" not in request.args:
        logging.error("No code found in request args")
        return redirect(url_for("index"))

    code = request.args.get("code")
    logging.info("Received authorization code: %s", code)

    if not code:
        logging.error("Code is None")
        return redirect(url_for("index"))

    try:
        # 记录请求详情
        request_data = {
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],  # 使用实际的 secret
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": url_for('callback', _external=True),
        }
        
        # 添加更多的请求头
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Python/requests"
        }
        
        logging.info("Sending token request to GitLab")
        token_response = requests.post(
            "http://127.0.0.1:9999/oauth/token",
            headers=headers,
            json=request_data,  # 使用 json 而不是 data
            timeout=10,
        )
        
        logging.info("Token response status code: %s", token_response.status_code)
        logging.info("Token response headers: %s", dict(token_response.headers))
        
        if token_response.status_code != 200:
            logging.error("Token request failed with status code: %s", token_response.status_code)
            logging.error("Response content: %s", token_response.text)
            # 添加更详细的错误信息
            if token_response.status_code == 503:
                logging.error("GitLab service is unavailable")
            elif token_response.status_code == 401:
                logging.error("Invalid client credentials")
            elif token_response.status_code == 400:
                logging.error("Invalid request parameters")
            return redirect(url_for("index"))
            
        token_json = token_response.json()
        logging.info("Token response parsed successfully: %s", {k: '***' if k == 'access_token' else v for k, v in token_json.items()})
        
        access_token = token_json.get("access_token")
        if not access_token:
            logging.error("Access token not found in response")
            return redirect(url_for("index"))
            
        logging.info("Access token received successfully")
        
    except requests.exceptions.RequestException as e:
        logging.error("Request exception during token request: %s", str(e))
        return redirect(url_for("index"))
    except json.JSONDecodeError as e:
        logging.error("JSON decode error: %s", str(e))
        logging.error("Raw response content: %s", token_response.text)
        return redirect(url_for("index"))
    except Exception as e:
        logging.error("Unexpected error during token request: %s", str(e))
        return redirect(url_for("index"))

    session["access_token"] = access_token
    logging.info("Access token stored in session successfully")
    return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Endpoint for the dashboard page.
    """
    access_token = session.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    logging.info("access_token: %s", access_token)
    user_response = requests.get(
        "http://127.0.0.1:9999/api/v4/user", headers=headers, timeout=10
    )
    user_data = user_response.json()
    logging.info("user_data: %s", user_data)

    username = user_data.get("username")
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

    access_token = str(data.get("access_token"))
    username = str(data.get("username"))
    timezone = str(data.get("timezone"))
    year = int(data.get("year"))

    if (not all([access_token, username, timezone, year])) or year < 2008 or year > 2030:
        return jsonify({"redirect_url": url_for("index")})
        
    session["access_token"] = access_token
    session["username"] = username
    session["timezone"] = timezone
    session["year"] = year

    try:
        requested_user = RequestedUser(username=username)
        db.session.add(requested_user)
        db.session.commit()
    except Exception as e:
        logging.error("Error saving requested user: %s", e)

    if not all([username, access_token, year, timezone]):
        return jsonify({"redirect_url": url_for("index", year=year)})

    def fetch_data():
        with app.app_context():
            try:
                context = get_context(username, access_token, year, timezone)

                logging.info("Context of %s: %s", username, json.dumps(context))
                
                user_context = UserContext(username=username, context=json.dumps(context))
                db.session.add(user_context)
                db.session.commit()
            except Exception as e:
                logging.error("Error fetching data: %s", e)

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

    logging.info("Display user context: %s", username)

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
    app.run(host="127.0.0.1", port=5000)
