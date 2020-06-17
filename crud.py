"""CRUD operations."""

from model import connect_to_db, db, User, Activity, Team, Team_Member, Comment
from datetime import datetime, timedelta
from pytz import timezone

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

def create_activity(user_id, strava_activity_id, date_utc, date_local,
                    desc, exercise_type, distance, workout_time,
                    average_speed, has_heartrate, effort, 
                    effort_source, elev_gain):
    """Create and return an activity."""

    activity = Activity(user_id=user_id,
                strava_activity_id=strava_activity_id,
                date_utc=date_utc,
                date_local=date_local,
                desc=desc,
                exercise_type=exercise_type,
                distance=distance,
                workout_time=workout_time,
                average_speed=average_speed,
                has_heartrate=has_heartrate,
                effort=effort,
                effort_source=effort_source,
                elev_gain=elev_gain
                )

    db.session.add(activity)
    db.session.commit()

    return activity

def create_team(name, coach_id, logo, team_banner_img, team_color):
    """Create and return a team."""
    
    team = Team(name=name, 
                coach_id=coach_id,
                logo=logo,
                team_banner_img=team_banner_img,
                team_color=team_color)

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

def create_comment(activity_id, author_id, date_utc, body):
    """Create and return a comment."""

    comment = Comment(activity_id=activity_id, 
                        author_id=author_id,
                        date_utc=date_utc,
                        body=body)

    db.session.add(comment)
    db.session.commit()

    return comment

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_activities_by_user_id(user_id):
    """Return a user by email."""

    return Activity.query.filter(Activity.user_id == user_id).all()

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

def get_athletes_by_team(team_id):
    """Return team members on a team."""

    return Team_Member.query.filter(Team_Member.team_id == team_id, Team_Member.role == 'Athlete').all()

# def get_activities_by_team(team_id):
#     """Return a list of activities completed by users on a team."""

#     athletes = get_athletes_by_team(team_id)

#     athlete_ids = []

#     for athlete in athletes:
#         athlete_ids.append(athlete.id)

#     activities = Activity.query.filter(Activity.user_id.in_(athlete_ids), Activity.exercise_type == 'Run').all()

#     activities_json = []

#     for activity in activities: 
#         act_dict = {"user_id" : activity.user_id,
#                 "strava_activity_id" : activity.strava_activity_id,
#                 "date" : activity.date_utc.strftime('%Y-%m-%d'),
#                 "day_of_week" : activity.date_utc.astimezone(timezone(user_timezone)).weekday(),
#                 "desc" : activity.desc,
#                 "exercise_type" : activity.exercise_type,
#                 "distance" : activity.distance,
#                 "workout_time" : activity.workout_time,
#                 "average_speed" : activity.average_speed,
#                 "effort" : activity.effort,
#                 "effort_source" : activity.effort_source,
#                 "elev_gain" : activity.elev_gain} 
#         activities_json.append(act_dict)

#     return activities_json
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

def get_current_week_activities(team_id, user_timezone):
    """Return a list of activities completed by users on a team during the current week."""

    today = datetime.utcnow().astimezone(timezone(user_timezone)) - timedelta(days=2)
    today = datetime(year=today.year, month=today.month,
                    day=today.day, hour=23, minute= 59, second=59)
    print("today is", today)
    monday = today - timedelta(days=today.weekday())
    monday = datetime(year=monday.year, month=monday.month,
                    day=monday.day, hour=0, minute=0, second=0)
    print("monday is", monday)
    athletes = get_athletes_by_team(team_id)

    athlete_ids = []

    curr_week_activities = {}

    for athlete in athletes:
        athlete_ids.append(athlete.id)

    activities = Activity.query.filter(Activity.date_local >= monday, Activity.date_local <= today, Activity.user_id.in_(athlete_ids)).all()

    weekdays = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday', 6: 'sunday'}


    for ath_id in athlete_ids:
        curr_week_activities[ath_id] = {'monday': {'Run':{'distance': '-'}, 'Cross Train':{'workout_time': '-'}},
                                        'tuesday': {'Run':{'distance': '-'}, 'Cross Train':{'workout_time': '-'}},
                                        'wednesday': {'Run':{'distance': '-'}, 'Cross Train':{'workout_time': '-'}},
                                        'thursday': {'Run':{'distance': '-'}, 'Cross Train':{'workout_time': '-'}},
                                        'friday': {'Run':{'distance': '-'}, 'Cross Train':{'workout_time': '-'}},
                                        'saturday': {'Run':{'distance': '-'}, 'Cross Train':{'workout_time': '-'}},
                                        'sunday': {'Run':{'distance': '-'}, 'Cross Train':{'workout_time': '-'}},
                                        'total_mileage': 0,
                                        'total_xtrain_mins': 0}

    for activity in activities:

        if activity.exercise_type == 'Run':

            curr_week_activities[activity.user_id]['total_mileage'] += activity.distance

            curr_week_activities[activity.user_id][weekdays[activity.date_local.weekday()]]['Run'] = {"date_local" : activity.date_local.strftime('%Y-%m-%d'),
                                                                                                    "desc" : activity.desc,
                                                                                                    "distance" : f'{activity.distance} mi',
                                                                                                    "workout_time" : convert_time_format(activity.workout_time),
                                                                                                    "average_speed" : activity.average_speed,
                                                                                                    "effort" : activity.effort,
                                                                                                    "effort_source" : activity.effort_source,
                                                                                                    "elev_gain" : activity.elev_gain}
        elif activity.exercise_type != 'Run':

            curr_week_activities[activity.user_id]['total_xtrain_mins'] += activity.workout_time

            curr_week_activities[activity.user_id][weekdays[activity.date_utc.weekday()]]['Cross Train'] = {"date_utc" : activity.date_local.strftime('%Y-%m-%d'),
                                                                                                            "exercise_type" : activity.exercise_type,
                                                                                                            "desc" : activity.desc,
                                                                                                            "distance" : f'{activity.distance} mi',
                                                                                                            "workout_time" : convert_time_format(activity.workout_time),
                                                                                                            "average_speed" : activity.average_speed,
                                                                                                            "effort" : activity.effort,
                                                                                                            "effort_source" : activity.effort_source,
                                                                                                            "elev_gain" : activity.elev_gain}
    for ath_id in athlete_ids:
        print("athlete id: ", ath_id, curr_week_activities[ath_id]['total_xtrain_mins'])
        print("athlete id: ", ath_id, type(curr_week_activities[ath_id]['total_xtrain_mins']))
        curr_week_activities[ath_id]['total_xtrain_mins'] = convert_time_format(curr_week_activities[ath_id]['total_xtrain_mins'])
        print("athlete id: ", ath_id, curr_week_activities[ath_id]['total_xtrain_mins'])

    return curr_week_activities


if __name__ == '__main__':
    from server import app
    connect_to_db(app)