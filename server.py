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

# from crud import create_user

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

# @app.route('/')
# def homepage():
#     # if 'username' in session:
#     #     return redirect(url_for('/dashboard'))
#     return render_template('homepage.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

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
    print(user)

    team = crud.get_team_by_user_id(user.id)

    if user == None:
        flash('Account does not exist. Please register as a new user.')
        return redirect('/')

    elif user.password != password:
        flash('Incorrect password. Please try again.')
        return redirect('/')

    elif user.password == password:
        session['user'] = email
        print(session['user'])
        activities = crud.get_activities_by_user_id(user.id)
        return render_template('team_dashboard.html', team=team, user=user, activities=activities)
    

@app.route("/create-user", methods=['POST'])
def create_user():

    email = request.form.get('email')
    password = request.form.get('password')
    password_confirm = request.form.get('password-confirm')
    phone = request.form.get('phone')
    token = request.form.get('token')
    token = ast.literal_eval(token)

    user = crud.get_user_by_email(email)

    if user != None:
        flash('Account already exists with provided email. Please login.')
        return redirect('/')

    else:
        user_data = strava_api.get_user_data()

        user = crud.create_user(user_data.firstname,
                        user_data.lastname,
                        phone,
                        email,
                        password,
                        user_data.profile,
                        user_data.id,
                        token['access_token'],
                        token['expires_at'],
                        token['refresh_token'])
        print(user)
        session['user_id'] = user.id
        session['user'] = user.email

        return redirect('/create-activities')
        

@app.route("/create-activities")
def create_activities():

    activity_data = strava_api.get_activity_data()

    for activity in activity_data:

        distance_in_miles = round(activity.distance.num *  0.000621371, 2)

        time = activity.moving_time.seconds / 3600
        hours = int(time)
        minutes = int((time % 1) * 60)
        seconds = round((((time % 1) * 60) % 1) * 60)
        if hours < 1:
            workout_time = f'{minutes}m {seconds}s'
        else:
            workout_time = f'{hours}h {minutes}m {seconds}s'

        avg_time = activity.moving_time.seconds / distance_in_miles
        avg_minutes = int(avg_time)
        avg_seconds = round((avg_time % 1) * 60)
        average_speed = f'{avg_minutes}:{avg_seconds}/mile'

        if activity.has_heartrate:
            effort_source = 'heartrate'
        else:
            effort_source = 'perceived exertion'
        if activity.suffer_score:
            effort = activity.suffer_score
        else:
            effort = 0

        print('-'*20)
        crud.create_activity(session['user_id'],
                            activity.id,
                            activity.start_date,
                            activity.name,
                            activity.type,
                            distance_in_miles,
                            workout_time,
                            average_speed,
                            activity.has_heartrate,
                            effort.real,
                            effort_source,
                            activity.total_elevation_gain.num)

    return redirect('/join-team')

@app.route('/join-team')
def get_teams():

    teams = crud.get_teams()

    return render_template('register_team.html', teams=teams)

@app.route('/create-team-mem', methods=['POST'])
def create_team_mem():

    team = request.form.get('team')
    team = crud.get_team_by_id(int(team))

    #convert team from string to object

    role = request.form.get('role')

    crud.create_team_member(session['user_id'], team.id, role)

    activities = crud.get_activities_by_user_id(session['user_id'])
    user = crud.get_user_by_email(session['user'])

    return render_template('team_dashboard.html', team=team,
                                            activities=activities,
                                            user=user)


        # token_url = "https://www.strava.com/oauth/token"
        # activities_url = "https://www.strava.com/api/v3/athlete/activities"

        # payload = {
        #     'client_id': 48415,
        #     'client_secret': 'ed4c1b2fa87eb5d3120bbb2a8a9c0f39451ca920',
        #     'refresh_token': user.strava_refresh_token,
        #     'grant_type': "refresh_token",
        #     'f': 'json'
        # }

        # print("Requesting Token...\n")
        # res = requests.post(token_url, data=payload, verify=False)
        # access_token = res.json()['access_token']
        # print("Access Token = {}\n".format(access_token))

        # header = {'Authorization': 'Bearer ' + access_token}
        # param = {'per_page': 200, 'page': 1}
        # my_dataset = requests.get(activities_url, headers=header, params=param).json()

        # print(token)
        # print("Access Token: ", token['access_token'])
        # print("Refresh Token: ", token['refresh_token'])

# # ... time passes ...
# if time.time() > client.token_expires_at:
#     refresh_response = client.refresh_access_token(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET,
#         refresh_token=client.refresh_token)
#     access_token = refresh_response['access_token']
#     refresh_token = refresh_response['refresh_token']
#     expires_at = refresh_response['expires_at']


# token_url = "https://www.strava.com/oauth/token"
# activites_url = "https://www.strava.com/api/v3/athlete/activities"

# payload = {
#     'client_id': 48415,
#     'client_secret': 'ed4c1b2fa87eb5d3120bbb2a8a9c0f39451ca920',
#     'refresh_token': user.strava_refresh_token,
#     'grant_type': "refresh_token",
#     'f': 'json'
# }

# print("Requesting Token...\n")
# res = requests.post(token_url, data=payload, verify=False)
# access_token = res.json()['access_token']
# print("Access Token = {}\n".format(access_token))

# header = {'Authorization': 'Bearer ' + access_token}
# param = {'per_page': 200, 'page': 1}
# my_dataset = requests.get(activites_url, headers=header, params=param).json()

# print(my_dataset[0]["name"])


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)