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

        firstname = user['firstname']
        lastname = user['lastname']
        phone = user['phone']
        email = user['email']
        password = user['password']
        timezone = user['timezone']

        if not 'id' in user:
            prof_pic = None
            strava_id = None
            strava_access_token = None
            strava_access_token_expir = None
            strava_refresh_token = None
        else:
            prof_pic = user['profile']
            strava_id = user['id']
            strava_access_token = user['access_token']
            strava_access_token_expir = user['expires_at']
            strava_refresh_token = user['refresh_token']

        crud.create_user(firstname, lastname, phone, email, password, prof_pic, timezone, 
                        strava_id, strava_access_token, strava_access_token_expir, 
                        strava_refresh_token)

def seed_activities():

    with open('data/activities.json') as f:
        activity_data = json.loads(f.read())

    for activity in activity_data:

        user = User.query.filter(User.strava_id==activity['athlete']['id']).first()
        user_id = user.id
        strava_activity_id = activity['id']
        date_utc = activity['start_date']
        date_local = activity['start_date_local']
        desc = activity['name']
        exercise_type = activity['type']
        distance = round(activity['distance'] * 0.000621371, 2)

        workout_time = activity['moving_time']

        if distance < 0:
            avg_time = (activity['moving_time'] / 60) / distance
            avg_minutes = int(avg_time)
            avg_seconds = round((avg_time % 1) * 60)
            average_speed = f'{avg_minutes}:{avg_seconds}/mile'
        else:
            average_speed = 'N/A'

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

        crud.create_activity(user_id, strava_activity_id, date_utc, date_local, 
                    desc, exercise_type, distance, workout_time,
                    average_speed, has_heartrate, effort, 
                    effort_source, elev_gain)

def seed_teams():

    with open('data/teams.json') as f:
        team_data = json.loads(f.read())

    for team in team_data:

        name = team['name']
        coach_id = team['coach_id']
        logo = team['logo']
        team_banner_img = team['team_banner_img']
        team_color = team['team_color']

        crud.create_team(name, coach_id, logo, team_banner_img, team_color)

def seed_team_members():

    with open('data/team_members.json') as f:
        team_member_data = json.loads(f.read())

    for member in team_member_data:

        user_id = member['user_id']
        team_id = member['team_id']
        role = member['role']

        crud.create_team_member(user_id, team_id, role)

def seed_comments():

    with open('data/comments.json') as f:
        comment_data = json.loads(f.read())

    for comment in comment_data:

        activity_id = comment['activity_id']
        author_id = comment['author_id']
        date_utc = comment['date_utc']
        body = comment['body']

        crud.create_comment(activity_id, author_id, date_utc, body)

seed_users()
seed_activities()
seed_teams()
seed_team_members()
seed_comments()


