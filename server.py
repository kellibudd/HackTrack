"""Server for team running app."""

from flask import (
    Flask,
    render_template,
    request,
    flash,
    session,
    redirect,
    url_for,
    jsonify,
)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
import strava_api
import os
import ast
from datetime import datetime

# from crud import create_user

app = Flask(__name__)
app.secret_key = os.environ["APP_SECRET_KEY"]
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():

    url = strava_api.request_user_authorization(
        url_for(".register_user", _external=True)
    )

    return render_template("homepage.html", authorize_url=url)


@app.route("/register")
def register_user():
    """Register a new user."""

    code = request.args.get("code")
    token = strava_api.get_token(code)

    return render_template("register_user.html", token=token)


@app.route("/login", methods=["POST"])
def login_user():
    """Login a user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user is None:
        flash(u"Account does not exist.", "email-error")
        return redirect("/")

    elif user.password != password:
        flash(u"Incorrect password. Please try again.", "password-error")
        return redirect("/")

    elif user.password == password:
        session["user"] = email
        session["user_id"] = user.id
        print("user logged in: ", session["user_id"])
        return redirect("/create-activities")


@app.route("/logout")
def logout_user():

    if "user" in session:
        session["user"]

    session.pop("user", None)

    return redirect("/")


@app.route("/create-user", methods=["POST"])
def create_user():

    email = request.form.get("email")
    password = request.form.get("password")
    password_confirm = request.form.get("password-confirm")
    phone = request.form.get("phone")
    token = request.form.get("token")
    token = ast.literal_eval(token)

    user = crud.get_user_by_email(email)

    if user is not None:
        flash(
            u"Account already exists with provided email. Please login.",
            "email-error",
        )

        return redirect(request.referrer)

    elif password != password_confirm:
        flash(
            u"Passwords do not match. Please try again.",
            "confirm-password-error",
        )

        return redirect(request.referrer)

    else:
        user_data = strava_api.get_strava_user_data()

        user = crud.create_user(
            user_data.firstname,
            user_data.lastname,
            phone,
            email,
            password,
            user_data.profile,
            user_data.id,
            token["access_token"],
            token["expires_at"],
            token["refresh_token"],
        )
        session["user"] = user.email
        session["user_id"] = user.id

        return redirect("/join-team")


@app.route("/join-team")
def get_teams():

    teams = crud.get_teams()

    return render_template("register_team.html", teams=teams)


@app.route("/create-team-mem", methods=["POST"])
def create_new_team_mem():

    team_id = int(request.form.get("team"))

    role = request.form.get("role")

    crud.create_team_member(session["user_id"], team_id, role)

    return redirect("/create-activities")


@app.route("/create-team", methods=["POST"])
def create_new_team():

    team_name = request.form.get("team_name")

    role = request.form.get("role")

    last_updated = datetime.utcnow()

    team = crud.create_team(team_name, session["user_id"], last_updated)

    crud.create_team_member(session["user_id"], team.id, role)

    return redirect("/create-activities")


@app.route("/create-activities", methods=["GET", "POST"])
def create_activities():

    user_team_role = crud.get_user_role(session["user_id"])

    if (
        crud.get_activities_by_user_id(session["user_id"]) == []
        and user_team_role == "Athlete"
    ):
        athlete = crud.get_user_by_email(session["user"])

        activities = strava_api.get_strava_activities_for_new_user(athlete)

        for activity in activities:

            if activity["type"] == "Run":
                activity = crud.create_activity(activity)
                print("ADDED: ", activity.desc)

    team = crud.get_team_by_user_id(session["user_id"])

    crud.update_team_activities(team.id)

    return redirect("/dashboard")


@app.route("/dashboard")
def display_team_dashboard():

    team = crud.get_team_by_user_id(session["user_id"])

    return render_template("team_dashboard.html", team=team)


@app.route("/dashboard/<date>")
def get_dashboard_week(date):

    team = crud.get_team_by_user_id(session["user_id"])

    return render_template("team_dashboard.html", team=team)


@app.route("/get-team-data")
def get_team_data():

    team = crud.get_team_by_user_id(session["user_id"])
    athletes = crud.get_athletes_on_team(team.id)

    return jsonify(athletes)


@app.route("/api/get-activity-data/<date>")
def get_activity_data(date):

    print(date)
    print(type(date))
    date = datetime.strptime(date, "%Y-%m-%d")
    print(date)
    print(type(date))
    week = date.isocalendar()[1]
    print(week)
    team = crud.get_team_by_user_id(session["user_id"])
    activities = crud.get_week_activities_json(team.id, week)

    return jsonify(activities)


@app.route("/add-comment", methods=["POST"])
def add_comment():

    strava_activity_id = request.form.get("activity-id")
    comment = request.form.get("comment")
    activity = crud.get_activity_by_strava_id(strava_activity_id)

    crud.create_comment(
        activity.id,
        session["user_id"],
        activity.user_id,
        datetime.utcnow(),
        comment,
    )

    return redirect(request.referrer)


@app.route("/api/get-comments/<int:activity_id>")
def get_comments(activity_id):

    comments = crud.get_comments_by_strava_activity_id(activity_id)
    print(comments)
    return jsonify(comments)


@app.route("/get-incoming-comments")
def get_incoming_comments():

    comments = crud.get_comments_to_user(session["user_id"])

    return jsonify(comments)


@app.route("/get-outgoing-comments")
def get_outgoing_comments():

    comments = crud.get_comments_from_user(session["user_id"])

    return jsonify(comments)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
