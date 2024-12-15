from util import Github
from generator.generate import generate_site
from generator.fetch import fetch_github

from flask import (
    Flask,
    request,
    url_for,
    render_template,
    send_from_directory,
    send_file,
    jsonify,
)
from io import BytesIO


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("loading.html")


@app.route("/load_data", methods=["POST"])
def load_data():
    data = request.json

    global access_token, username, timezone, year
    access_token = data.get("access_token")
    username = data.get("username")
    timezone = data.get("timezone")
    year = int(data.get("year"))

    github = Github(access_token, username, timezone)

    result, result_new_repo = fetch_github(github, year, skip_fetch=False)

    global avatar, html_output
    avatar, html_output = generate_site(year, result, result_new_repo)

    return jsonify({"redirect_url": url_for("get_2024", year=year)})


@app.route("/2024")
def get_2024():
    return html_output


@app.route("/avatar.png")
def avatar():
    return send_file(BytesIO(avatar), mimetype="image/png")


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)
