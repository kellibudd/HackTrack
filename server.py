"""Server for team running app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for, jsonify)
from model import connect_to_db, User, Activity, Team, Comment
import crud
from jinja2 import StrictUndefined
import strava_api
import os
import json
import ast
from datetime import datetime, timedelta
from pytz import timezone

# from crud import create_user

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():

    url = strava_api.request_user_authorization(url_for('.register_user', _external=True))

    return render_template('homepage.html', authorize_url=url)


@app.route('/register')
def register_user():
    """Register a new user."""

    code = request.args.get('code')
    token = strava_api.get_token(code)

    return render_template('register_user.html', token=token)


@app.route('/login', methods=['POST'])
def login_user():
    """Login a user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user == None:
        flash('Account does not exist. Please register as a new user.')
        return redirect('/')

    elif user.password != password:
        flash('Incorrect password. Please try again.')
        return redirect('/')

    elif user.password == password:
        session['user'] = email
        session['user_id'] = user.id
        return redirect('/create-activities')


@app.route('/logout')
def logout_user():
    
    error = None

    if "user" in session:
        user = session['user']

    session.pop("user", None)

    return redirect('/')
    

@app.route("/create-user", methods=['POST'])
def create_user():

    email = request.form.get('email')
    password = request.form.get('password')
    password_confirm = request.form.get('password-confirm')
    phone = request.form.get('phone')
    timezone = request.form.get('timezone')
    token = request.form.get('token')
    token = ast.literal_eval(token)

    user = crud.get_user_by_email(email)

    if user != None:
        flash('Account already exists with provided email. Please login.')
        return redirect('/')

    else:
        user_data = strava_api.get_strava_user_data()

        user = crud.create_user(user_data.firstname,
                                user_data.lastname,
                                phone,
                                email,
                                password,
                                user_data.profile,
                                timezone,
                                user_data.id,
                                token['access_token'],
                                token['expires_at'],
                                token['refresh_token'])
        session['user'] = user.email
        session['user_id'] = user.id
        session['timezone'] = user.timezone

        return redirect('/join-team')


@app.route('/join-team')
def get_teams():

    teams = crud.get_teams()

    return render_template('register_team.html', teams=teams)


@app.route('/create-team-mem', methods=['POST'])
def create_new_team_mem():

    team_id = int(request.form.get('team'))

    role = request.form.get('role')

    team_mem = crud.create_team_member(session['user_id'], team_id, role)

    return redirect('/create-activities')


@app.route('/create-activities', methods=['GET','POST'])
def create_activities():

    if crud.get_activities_by_user_id(session['user_id']) == None:

        athlete = crud.get_user_by_email(session['user'])

        activities = crud.get_strava_activities(athlete)

        for activity in activities:
            crud.create_activity(activity)

    team = crud.get_team_by_user_id(session['user_id'])

    if datetime.utcnow() - team.activities_last_updated > timedelta(0, 10800):
        print("Updating team activities...")
        crud.update_team_activities(team.id)

    return redirect('/dashboard')    

@app.route('/dashboard')
def display_team_dashboard():

    return render_template('team_dashboard.html')

@app.route('/get-team-data')
def get_team_data():

    team = crud.get_team_by_user_id(session['user_id'])
    athletes = crud.get_athletes_on_team(team.id)

    return jsonify(athletes)

@app.route('/get-activity-data')
def get_activity_data():

    team = crud.get_team_by_user_id(session['user_id'])
    activities = crud.get_week_activities_json(team.id, 25)

    return jsonify(activities)

@app.route('/api/get-activity-splits/<int:activity_id>')
def get_activity_splits(activity_id):

    athlete = crud.get_athlete_by_activity(activity_id)
   
    if datetime.fromtimestamp(int(athlete.strava_access_token_expir)) < datetime.utcnow():
        crud.get_new_access_token_for_user(athlete)

    split_data = strava_api.get_strava_activities_with_laps(athlete, activity_id)

    return jsonify(split_data)

# @app.route('/get-week-activities')
# def get_week_activities():

#     activities_dict = crud.get_week_activities_json(team.id, week)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)