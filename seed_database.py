"""A database."""

import os, server, crud, json
from model import connect_to_db, db, User, Activity, Team, Team_Member, Comment
from datetime import datetime

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

        crud.create_user(firstname, lastname, phone, email, password, prof_pic, 
                        strava_id, strava_access_token, strava_access_token_expir, 
                        strava_refresh_token)

# def seed_activities():

#     with open('data/activities.json') as f:
#         activity_data = json.loads(f.read())

#     for activity in activity_data:
#         athlete = User.query.filter(User.strava_id==activity['athlete']['id']).first()

#         date = datetime.strptime(activity['start_date_local'].split('T')[0], '%Y-%m-%d')
        
#         new_activity = Activity(user_id=athlete.id,
#                         strava_activity_id=activity['id'],
#                         date_utc=activity['start_date'],
#                         date_local=activity['start_date_local'],
#                         week_num=date.isocalendar()[1],
#                         weekday=date.isocalendar()[2],
#                         desc=activity['name'],
#                         exercise_type=activity['type'],
#                         distance=activity['distance'],
#                         workout_time=activity['moving_time'],
#                         elev_gain=activity['total_elevation_gain'])

#         db.session.add(new_activity)
#         db.session.commit()

def seed_teams():

    with open('data/teams.json') as f:
        team_data = json.loads(f.read())

    for team in team_data:

        team = Team(name=team['name'], 
                    coach_id=team['coach_id'],
                    logo=team['logo'],
                    team_banner_img=team['team_banner_img'],
                    team_color=team['team_color'],
                    activities_last_updated=team['activities_last_updated'])

        db.session.add(team)
        db.session.commit()

def seed_team_members():

    with open('data/team_members.json') as f:
        team_member_data = json.loads(f.read())

    for member in team_member_data:

        user_id = member['user_id']
        team_id = member['team_id']
        role = member['role']

        crud.create_team_member(user_id, team_id, role)

# def seed_comments():

#     with open('data/comments.json') as f:
#         comment_data = json.loads(f.read())

#     for comment in comment_data:

#         activity_id = comment['activity_id']
#         author_id = comment['author_id']
#         recipient_id = comment['recipient_id']
#         date_utc = comment['date_utc']
#         body = comment['body']

#         crud.create_comment(activity_id, author_id, recipient_id, date_utc, body)

seed_users()
# seed_activities()
seed_teams()
seed_team_members()
# seed_comments()


