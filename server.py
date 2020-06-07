"""Server for team running app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for, jsonify)
from model import connect_to_db, User, Activity, Team, Comment
import crud
from jinja2 import StrictUndefined
from stravalib import Client
import requests
import os
import urllib3
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# from crud import create_user

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# STRAVA_CLIENT_ID = os.environ['STRAVA_CLIENT_ID']
# STRAVA_CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']

@app.route("/")
def login():
    client = Client()
    url = client.authorization_url(client_id=48415,
                                    redirect_uri=url_for('.logged_in', _external=True),
                                    approval_prompt='auto')
    return render_template('login.html', authorize_url=url)


@app.route("/strava-oauth")
def logged_in():
    """
    Method called by Strava (redirect) that includes parameters.
    - state
    - code
    - error
    """
    error = request.args.get('error')
    state = request.args.get('state')
    if error:
        return render_template('login_error.html', error=error)
    else:
        code = request.args.get('code')
        print(code)
        client = Client()
        token = client.exchange_code_for_token(client_id=48415,
                                                client_secret='ed4c1b2fa87eb5d3120bbb2a8a9c0f39451ca920',
                                                code=code)
        # Probably here you'd want to store this somewhere -- e.g. in a database.
        # token = access_token.json
        user = client.get_athlete()

        new_user = crud.create_user(user.firstname,
                                    user.lastname,
                                    user.username,
                                    user.profile,
                                    user.id,
                                    token['access_token'],
                                    token['expires_at'],
                                    token['refresh_token'])

        activities = client.get_activities()

        for activity in activities:
            if activity.has_heartrate:
                effort_source = 'heartrate'
            else:
                effort_source = 'perceived exertion'
            if activity.suffer_score:
                effort = activity.suffer_score
            else:
                effort = 0
            print('-'*20)
            print(crud.create_activity(new_user.id,
                                activity.id,
                                activity.start_date,
                                activity.name,
                                activity.type,
                                activity.workout_type,
                                activity.distance.num,
                                activity.moving_time.seconds,
                                activity.average_speed.num,
                                activity.max_speed.num,
                                activity.has_heartrate,
                                effort.real,
                                effort_source,
                                activity.total_elevation_gain.num))

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

        print(new_user)
        # print(token)
        # print("Access Token: ", token['access_token'])
        # print("Refresh Token: ", token['refresh_token'])

        return render_template('login_results.html', user=user, token=token)



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