from flask import (
    Flask,
    Blueprint,
    redirect,
    g,
    flash,
    render_template,
    request,
    url_for,
    session,
)

import requests

bp = Blueprint("home", __name__)


@bp.before_request
def before_request():
    if request.endpoint != "home.index":
        if "token" not in session:
            return redirect(url_for("home.index"))
        g.token = session["token"]


@bp.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        token = request.form["token"]
        error = None

        if not token:
            error = "No OAuth token provided"

        if error is None:
            session["token"] = token
            return redirect(url_for("home.playlists"))

        flash(error)

    return render_template("index.html")


@bp.route("/playlists", methods=("GET", "POST"))
def playlists():
    query = "https://api.spotify.com/v1/me/playlists"
    response = requests.get(
        query, headers={"Authorization": "Bearer {}".format(g.token)}
    )
    response_json = response.json()

    if response_json["error"]:
        flash(response_json["error"]["message"])
        return redirect(url_for("home.index"))
    print("res ", response_json)

    return render_template(
        "playlists.html", playlists=response_json["items"], token=g.token
    )
