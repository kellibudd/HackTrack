"""Models for team running app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    prof_pic = db.Column(db.String)
    timezone = db.Column(db.String)
    strava_id = db.Column(db.Integer)
    strava_access_token = db.Column(db.String)
    strava_access_token_expir = db.Column(db.String)
    strava_refresh_token = db.Column(db.String)

    teams = db.relationship('Team', backref='coach')
    activities = db.relationship('Activity', backref='user')

    def __repr__(self):
        return f'<User id={self.id} first={self.firstname} last={self.lastname}>'

class Team(db.Model):
    """A team."""

    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    logo = db.Column(db.String)
    team_banner_img = db.Column(db.String)
    team_color = db.Column(db.String)
    activities_last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Team id={self.id} name={self.name}>'

class Team_Member(db.Model):
    """A member of a team"""

    __tablename__ = 'team_members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    role = db.Column(db.String, nullable=False)
    active_status = db.Column(db.Boolean, default=True)
    injury_status = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='team_members')
    team = db.relationship('Team', backref='team_members')

    def __repr__(self):
        return f'''<Team_Member id={self.id} team_id={self.team_id} 
                role={self.role}>'''


class Activity(db.Model):
    """An activity."""

    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    strava_activity_id = db.Column(db.String, nullable=False, unique=True)
    date_utc = db.Column(db.DateTime, nullable=False)
    date_local = db.Column(db.DateTime, nullable=False)
    week_num= db.Column(db.Integer)
    weekday= db.Column(db.Integer)
    desc = db.Column(db.String)
    exercise_type = db.Column(db.String, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    workout_time = db.Column(db.Integer, nullable=False)
    elev_gain = db.Column(db.Integer)
    splits = db.Column(db.String)

    def __repr__(self):
        return f'''<Activity id={self.id} user={self.user_id} 
                date_utc={self.date_utc} exercise_type={self.exercise_type}>'''


class Comment(db.Model):
    """A comment."""

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_utc = db.Column(db.DateTime)
    body = db.Column(db.Text, nullable=False)

    # user = db.relationship('User', backref='comments')
    activity = db.relationship('Activity', backref='comments')


    def __repr__(self):
        return f'''<Comment id={self.id} activity_id={self.activity_id}
                    author_id={self.author_id} date={self.date_utc}>'''


def connect_to_db(flask_app, db_uri='postgresql:///run_app', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
