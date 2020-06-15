"""CRUD operations."""

from model import connect_to_db, db, User, Activity, Team, Team_Member, Comment
from datetime import datetime, timedelta
from pytz import timezone

def create_user(firstname, lastname, phone, email, password, prof_pic, strava_id, 
                strava_access_token, strava_access_token_expir, strava_refresh_token):
    """Create and return a user."""

    user = User(firstname=firstname,
                lastname=lastname,
                phone=phone,
                email=email,
                password=password,
                prof_pic=prof_pic,
                strava_id=strava_id,
                strava_access_token=strava_access_token,
                strava_access_token_expir=strava_access_token_expir,
                strava_refresh_token=strava_refresh_token
                )

    db.session.add(user)
    db.session.commit()

    return user

def create_activity(user_id, strava_activity_id, date_utc, 
                    desc, exercise_type, distance, time_length,
                    average_speed, has_heartrate, effort, 
                    effort_source, elev_gain):
    """Create and return an activity."""

    activity = Activity(user_id=user_id,
                strava_activity_id=strava_activity_id,
                date_utc=date_utc,
                desc=desc,
                exercise_type=exercise_type,
                distance=distance,
                time_length=time_length,
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

    return Team_Member.query.options(db.joinedload('user')).filter(Team_Member.team_id == team_id, Team_Member.role == 'Athlete').all()

def get_activities_by_team(team_id):
    """Return a list of activities completed by users on a team."""

    team = Team_Member.query.filter(Team_Member.team_id == team_id, Team_Member.role == 'Athlete').all()

    team_activities = []

    for athlete in team:
        team_activities = team_activities + Activity.query.options(db.joinedload('user')).filter(Activity.user_id == athlete.user_id).all()
        # team_activities[athlete.id] = Activity.query.filter(Activity.user_id == athlete.user_id).all()

    return team_activities

def current_week_activities_by_team(team_id):
    """Return a list of activities completed by users on a team during the current week."""

    today = datetime.utcnow().astimezone(timezone('US/Pacific'))

    start = today - timedelta(days=today.weekday())

    current_week = []

    for i in range(7):

        day = start + timedelta(days=i)
        current_week.append(day.strftime('%Y-%m-%d'))

    team_activities = get_activities_by_team(team_id)

    current_week_activities = []

    for activity in team_activities: 
        date_pst = activity.date_utc.astimezone(timezone('US/Pacific')).strftime('%Y-%m-%d') 
        if date_pst in current_week: 
            current_week_activities.append(activity)

    return current_week_activities


if __name__ == '__main__':
    from server import app
    connect_to_db(app)