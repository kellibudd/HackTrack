"""Strava API"""

from flask import Flask, url_for, redirect
import server
import requests
import os
import urllib3
from stravalib import Client
import logging
import crud
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

STRAVA_CLIENT_ID = os.environ['STRAVA_CLIENT_ID']
STRAVA_CLIENT_SECRET = os.environ['STRAVA_CLIENT_SECRET']

client = Client()

def request_user_authorization(redirect_uri):

    return client.authorization_url(client_id=STRAVA_CLIENT_ID,
                                    redirect_uri=redirect_uri,
                                    approval_prompt='auto',
                                    scope='activity:read_all')

def get_token(code):

    return client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID,
                                            client_secret=STRAVA_CLIENT_SECRET,
                                            code=code)
def get_strava_user_data():

    return client.get_athlete()

def get_activity_data():

    return client.get_activities()

def get_new_token(refresh_token):

    return client.refresh_access_token(client_id=STRAVA_CLIENT_ID,
                                        client_secret=STRAVA_CLIENT_SECRET,
                                        refresh_token=refresh_token)

def get_strava_activities(athlete):

    team = crud.get_team_by_user_id(athlete.id)

    access_token = athlete.strava_access_token
    header = {'Authorization': 'Bearer ' + access_token}
    activities_url = 'https://www.strava.com/api/v3/athlete/activities'
    payload = {'after': int(team.activities_last_updated.timestamp()), 'per_page': 200}

    return requests.get(activities_url, headers=header, params=payload).json()

def get_strava_activities_with_laps(strava_access_token, strava_activity_id):

    access_token = strava_access_token
    header = {'Authorization': 'Bearer ' + access_token}
    id_as_int = strava_activity_id
    activities_url = f'https://www.strava.com/api/v3/activities/{id_as_int}' 

    return requests.get(activities_url, headers=header).json()
