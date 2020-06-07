"""Models for team running app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    # phone = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    # email = db.Column(db.String, nullable=False, unique=True)
    # password = db.Column(db.String, nullable=False)
    prof_pic = db.Column(db.String)
    strava_id = db.Column(db.String)
    strava_access_token = db.Column(db.String)
    strava_refresh_token = db.Column(db.String)

    team = db.relationship('Team', backref='users')
    activity = db.relationship('Activity', backref='users')

    def __repr__(self):
        return f'''<User id={self.id} first={self.firstname}
        last={self.lastname} username={self.username}>'''

class Team(db.Model):
    """A team."""

    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    logo = db.Column(db.String)
    team_color = db.Column(db.String)

    def __repr__(self):
        return f'<Team id={self.id} name={self.name}>'


class Activity(db.Model):
    """An activity."""

    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    strava_activity_id = db.Column(db.String, nullable=False)
    start_datetime_utc = db.Column(db.DateTime, nullable=False)
    desc = db.Column(db.String)
    exercise_type = db.Column(db.String, nullable=False)
    run_type = db.Column(db.String)
    distance = db.Column(db.Float, nullable=False)
    time_length = db.Column(db.Integer, nullable=False)
    avg_speed = db.Column(db.Float)
    max_speed = db.Column(db.Float)
    has_heartrate = db.Column(db.Boolean)
    effort = db.Column(db.Integer)
    effort_source = db.Column(db.String)
    elev_gain = db.Column(db.Integer)

    def __repr__(self):
        return f'''<Activity id={self.id} user={self.user_id} 
                date={self.date} exercise_type={self.exercise_type}>'''


class Comment(db.Model):
    """A comment."""

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    author_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime)
    body = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref='comments')
    activity = db.relationship('Activity', backref='comments')


    def __repr__(self):
        return f'''<Comment id={self.id} activity_id={self.activity_id}
                    author={self.author_user_id} date={self.date}>'''


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
