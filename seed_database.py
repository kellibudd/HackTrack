"""A database."""

import os, server, crud, json
from model import connect_to_db, db, User, Activity, Team, Team_Member, Comment

os.system('dropdb run_app')
os.system('createdb run_app')

connect_to_db(server.app)
db.create_all()

def seed_users():

    with open('data/users.json') as f:
        user_data = json.loads(f.read())

    for user in user_data:

        firstname = user['athlete']['firstname']
        lastname = user['athlete']['lastname']
        phone = user['athlete']['phone']
        email = user['athlete']['email']
        password = user['athlete']['password']
        prof_pic = user['athlete']['profile']
        strava_id = user['athlete']['id']
        strava_access_token = user['access_token']
        strava_access_token_expir = user['expires_at']
        strava_refresh_token = user['refresh_token']

        crud.create_user(firstname, lastname, phone, email, password, prof_pic, 
                        strava_id, strava_access_token, strava_access_token_expir, 
                        strava_refresh_token)

def seed_activities():

    with open('data/activities.json') as f:
        activity_data = json.loads(f.read())

    for activity in activity_data:

        user = User.query.filter(User.strava_id==activity['athlete']['id']).first()
        strava_activity_id = activity['id']
        date_utc = activity['start_date']
        desc = activity['name']
        exercise_type = activity['type']
        distance = activity['distance']
        time_length = activity['moving_time']
        average_speed = activity['average_speed']
        max_speed = activity['max_speed']
        has_heartrate = activity['has_heartrate']

        if activity['has_heartrate']:
            effort_source = 'heartrate'
        else:
            effort_source = 'perceived exertion'

        if not 'suffer_score' in activity:
            effort = 0
        else:
            effort = activity['suffer_score']

        elev_gain = activity['total_elevation_gain']

        print(user)
        print(strava_activity_id)
        print(date_utc)
        print(desc)
        print(exercise_type)
        print(distance)
        print(time_length)
        print(average_speed)
        print(max_speed)
        print(has_heartrate)
        print(effort) 
        print(effort_source)
        print(elev_gain)
        print('*'*20)

        crud.create_activity(user, strava_activity_id, date_utc, 
                    desc, exercise_type, distance, time_length,
                    average_speed, max_speed, has_heartrate, effort, 
                    effort_source, elev_gain)
