"""Strava API"""

from flask import Flask, url_for, redirect
import server
import requests
import os
import urllib3
from stravalib import Client
import logging
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
