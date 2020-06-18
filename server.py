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

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('/'))

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
        session['timezone'] = user.timezone
        return redirect('/dashboard')


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

        return redirect('/create-activities')


@app.route("/create-activities")
def create_activities():

    athlete = crud.get_user_by_email(email)

    activities = crud.get_strava_activities(athlete)

    for activity in activities:
        crud.create_activity(activity)

    return redirect('/join-team')


@app.route('/join-team')
def get_teams():

    teams = crud.get_teams()

    return render_template('register_team.html', teams=teams)


@app.route('/create-team-mem', methods=['POST'])
def create_team_mem():

    team_id = int(request.form.get('team'))

    role = request.form.get('role')

    team_mem = crud.create_team_member(session['user_id'], team_id, role)

    return redirect('/dashboard')
    

@app.route('/dashboard')
def display_team_dashboard():

    team = crud.get_team_by_user_id(session['user_id'])
    athletes = crud.get_all_athlete_data_by_team(team.id)
    activities_dict = crud.get_current_week_activities(team.id, session['timezone'])

    return render_template('team_dashboard.html', team=team, athletes=athletes, activities_dict=activities_dict)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)