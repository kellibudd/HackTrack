"""CRUD operations."""

from model import db, User

def create_user(firstname, lastname, username, prof_pic, strava_id, strava_access_token, strava_refresh_token):
    """Create and return a user."""

    user = User(firstname=firstname,
                lastname=lastname,
                username=username,
                prof_pic=prof_pic,
                strava_id=strava_id,
                strava_access_token=strava_access_token,
                strava_refresh_token=strava_refresh_token
                )

    db.session.add(user)
    db.session.commit()

    return user

if __name__ == '__main__':
    from server import app
    connect_to_db(app)