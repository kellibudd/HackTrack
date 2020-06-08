"""CRUD operations."""

from model import connect_to_db, db, User, Activity, Team, Team_Member, Comment

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
                    average_speed, max_speed, has_heartrate, effort, 
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
                max_speed=max_speed,
                has_heartrate=has_heartrate,
                effort=effort,
                effort_source=effort_source,
                elev_gain=elev_gain
                )

    db.session.add(activity)
    db.session.commit()

    return activity


if __name__ == '__main__':
    from server import app
    connect_to_db(app)