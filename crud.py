"""CRUD operations."""

from model import connect_to_db, db, User, Activity, Team, Team_Member, Comment
import requests
from datetime import datetime, timedelta
from pytz import timezone
import strava_api

def create_user(firstname, lastname, phone, email, password, prof_pic, timezone, strava_id, 
                strava_access_token, strava_access_token_expir, strava_refresh_token):
    """Create and return a user."""

    user = User(firstname=firstname,
                lastname=lastname,
                phone=phone,
                email=email,
                password=password,
                prof_pic=prof_pic,
                timezone=timezone,
                strava_id=strava_id,
                strava_access_token=strava_access_token,
                strava_access_token_expir=strava_access_token_expir,
                strava_refresh_token=strava_refresh_token
                )

    db.session.add(user)
    db.session.commit()

    return user


def create_activity(strava_activity):
    """Create and return an activity."""

    user = User.query.filter(User.strava_id==strava_activity['athlete']['id']).first()

    date = datetime.strptime(strava_activity['start_date_local'].split('T')[0], '%Y-%m-%d')

    new_activity = Activity(user_id=user.id,
                            strava_activity_id=strava_activity['id'],
                            date_utc=strava_activity['start_date'],
                            date_local=strava_activity['start_date_local'],
                            week_num=date.isocalendar()[1],
                            weekday=date.isocalendar()[2],
                            desc=strava_activity['name'],
                            exercise_type=strava_activity['type'],
                            distance=strava_activity['distance'],
                            workout_time=strava_activity['moving_time'],
                            elev_gain=strava_activity['total_elevation_gain'])

    db.session.add(new_activity)
    db.session.commit()

    return new_activity


def create_team(name, coach_id, logo, team_banner_img, team_color, activities_last_updated):
    """Create and return a team."""
    
    team = Team(name=name, 
                coach_id=coach_id,
                logo=logo,
                team_banner_img=team_banner_img,
                team_color=team_color,
                activities_last_updated=activities_last_updated)

    db.session.add(team)
    db.session.commit()

    return team


def create_team_member(user_id, team_id, role):
    """Create and return a team member."""
    
    team_member = Team_Member(user_id=user_id, 
                            team_id=team_id,
                            role=role)

    db.session.add(team_member)
    db.session.commit()

    return team_member


def create_comment(activity_id, author_id, recipient_id, date_utc, body):
    """Create and return a comment."""

    comment = Comment(activity_id=activity_id, 
                        author_id=author_id,
                        recipient_id=recipient_id,
                        date_utc=date_utc,
                        body=body)

    db.session.add(comment)
    db.session.commit()

    return comment

def get_comments_by_strava_activity_id(strava_id):

    activity = get_activity_by_strava_id(strava_id)

    comments = Comment.query.filter(Comment.activity_id==activity.id).order_by(Comment.date_utc.desc()).all()

    json = []

    for comment in comments:

        author = get_user_by_id(comment.author_id)
        recipient = get_user_by_id(comment.recipient_id)

        comment_dict = {'id': comment.id,
                        'activity_id': activity.id,
                        'author_name': f'{author.firstname} {author.lastname}',
                        'author_prof_pic': author.prof_pic,
                        'recipient_name': f'{recipient.firstname} {recipient.lastname}',
                        'recipient_prof_pic': recipient.prof_pic,
                        'date_utc': comment.date_utc,
                        'body': comment.body}
        json.append(comment_dict)

    return json

def get_comments_to_user(user_id):

    return Comment.query.filter(Comment.recipient_id==user_id).all()

def get_comments_from_user(user_id):

    return Comment.query.filter(Comment.author_id==user_id).all()

def get_all_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by email."""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_athlete_by_activity(activity_id):

    activity = Activity.query.filter(Activity.strava_activity_id == str(activity_id)).first()
    print(activity.user_id)
    return User.query.get(activity.user_id)


def get_activities_by_user_id(user_id):
    """Return a user by email."""

    return Activity.query.filter(Activity.user_id == user_id).all()

def get_activity_by_strava_id(activity_id):

    return Activity.query.filter(Activity.strava_activity_id == str(activity_id)).first()


def get_teams():
    """Return a list of teams."""

    return Team.query.all()


def get_team_by_id(id):
    """Return a team."""

    return Team.query.get(id)


def get_team_by_user_id(user_id):
    """Return team associated with a user."""

    team_mem = Team_Member.query.filter(Team_Member.user_id == user_id).first()

    return Team.query.filter(Team.id == team_mem.team_id).first()


def get_athlete_ids_by_team(team_id):
    """Return all user ids of members on a team."""

    athletes = Team_Member.query.filter(Team_Member.team_id == team_id, Team_Member.role == 'Athlete').all()

    athlete_ids = []

    for athlete in athletes:
        athlete_ids.append(athlete.user_id)

    return athlete_ids


def get_all_athlete_data_by_team(team_id):
    """Return user profile data of members on a team."""

    athletes = get_athlete_ids_by_team(team_id)

    return User.query.filter(User.id.in_(athletes)).all()

def get_new_access_token_for_user(athlete):
    """Update access token for a user"""

    token = strava_api.get_new_token(athlete.strava_refresh_token)
    athlete.strava_access_token = token['access_token']
    athlete.strava_access_token_expir = token['expires_at']
    db.session.commit()

def get_new_access_tokens_for_team(team_id):
    """Update access tokens for all users on a given team"""

    athletes = get_all_athlete_data_by_team(team_id)

    for athlete in athletes:
        get_new_access_token_for_user(athlete)

    updated_athlete_data = get_all_athlete_data_by_team(team_id)

    return updated_athlete_data


def show_strava_activities_in_db(team_id):

    athlete_ids = get_athlete_ids_by_team(team_id)

    activities = Activity.query.filter(Activity.user_id.in_(athlete_ids)).all()

    strava_activity_ids = set()

    for activity in activities:
        strava_activity_ids.add(activity.strava_activity_id)

    return strava_activity_ids

def update_team_activities(team_id):

    athletes = get_new_access_tokens_for_team(team_id)

    for athlete in athletes:
        activities = strava_api.get_strava_activities(athlete)
        
        for activity in activities:
            if not str(activity['id']) in show_strava_activities_in_db(team_id):
                create_activity(activity)
                print("*"*60)
                print("ADDED: ", activity['name'])
    
    team = get_team_by_id(team_id)
    team.activities_last_updated = datetime.utcnow()


def convert_time_format(time):

    time = time / 3600
    hours = int(time)
    minutes = int((time % 1) * 60)
    seconds = round((((time % 1) * 60) % 1) * 60)
    if hours < 1 and seconds > 10:
        return f'{minutes}:{seconds}'
    elif hours < 1 and seconds < 10:
        return f'{minutes}:0{seconds}'
    elif hours >= 1 and seconds > 10:
        return f'{hours}:{minutes}:{seconds}'
    else:
        return f'{hours}:{minutes}:0{seconds}'

def get_athletes_on_team(team_id):
    
    athlete_ids = get_athlete_ids_by_team(team_id)

    athletes = User.query.filter(User.id.in_(athlete_ids)).all()

    json = []

    for athlete in athletes:
        athlete_dict = {"id" : athlete.id,
                        "name": f'{athlete.firstname} {athlete.lastname}',
                        "prof_pic" : athlete.prof_pic}
        json.append(athlete_dict)

    return sorted(json, key = lambda i: i['name']) 

def get_week_activities_json(team_id, week):
    """Return a list of activities completed by users on a team during the current week."""

    athlete_ids = get_athlete_ids_by_team(team_id)

    activities = Activity.query.filter(Activity.week_num == week, Activity.user_id.in_(athlete_ids)).all()

    json = []

    for activity in activities: 
        act_dict = {"id" : activity.id,
                    "user_id" : activity.user_id,
                    "strava_activity_id" : activity.strava_activity_id,
                    "date" : activity.date_local,
                    "week" : activity.week_num,
                    "weekday" : activity.weekday,
                    "desc" : activity.desc,
                    "exercise_type" : activity.exercise_type,
                    "distance" : activity.distance,
                    "workout_time" : activity.workout_time,
                    "elev_gain" : activity.elev_gain}
        json.append(act_dict)

    return json


if __name__ == '__main__':
    from server import app
    connect_to_db(app)