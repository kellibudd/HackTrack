"""Server for team running app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for, jsonify)
from model import connect_to_db, User, Activity, Team, Comment
import crud
from jinja2 import StrictUndefined
import strava_api
import os

# from crud import create_user

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

# @app.route('/')
# def homepage():
#     # if 'username' in session:
#     #     return redirect(url_for('/dashboard'))
#     return render_template('homepage.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('/'))

@app.route('/')
def homepage():

    return render_template('homepage.html')

@app.route('/login', methods=['POST'])
def login_user():
    """Login a user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    print(user)

    if user == None:
        flash('Account does not exist. Please register as a new user.')
        return redirect('/')

    elif user.password != password:
        flash('Incorrect password. Please try again.')
        return redirect('/')

    elif user.password == password:
        session['user'] = email
        print(session['user'])
        return render_template('dashboard.html',user=user)

@app.route('/register', methods=['POST'])
def register_user():
    """Register a new user."""

    url = strava_api.request_user_authorization(url_for('.create_user', _external=True))

    return render_template('register.html', authorize_url=url)

@app.route("/create-user", methods=['POST'])
def create_user():

    email = request.form.get('email')
    password = request.form.get('password')
    password_confirm = request.form.get('password-confirm')
    phone = request.form.get('phone')

    code = request.args.get('code')
    token = strava_api.get_token(code)
    user_data = strava_api.get_user_data()

    if password != password_confirm:
        flash('Passwords do not match. Please try again.')
        return redirect('/register')

    else:
        user = crud.create_user(user_data.firstname,
                        user_data.lastname,
                        phone,
                        email,
                        password,
                        user_data.profile,
                        user_data.id,
                        token['access_token'],
                        token['expires_at'],
                        token['refresh_token'])

        session['user_id'] = user.id
        session['user'] = user.email

        return redirect('/create-activities')
        

@app.route("/create-activities")
def create_activities():

    activity_data = strava_api.get_activity_data()

    for activity in activity_data:

        if activity.has_heartrate:
            effort_source = 'heartrate'
        else:
            effort_source = 'perceived exertion'
        if activity.suffer_score:
            effort = activity.suffer_score
        else:
            effort = 0

        print('-'*20)
        crud.create_activity(session['user_id'],
                            activity.id,
                            activity.start_date,
                            activity.name,
                            activity.type,
                            activity.distance.num,
                            activity.moving_time.seconds,
                            activity.average_speed.num,
                            activity.max_speed.num,
                            activity.has_heartrate,
                            effort.real,
                            effort_source,
                            activity.total_elevation_gain.num)

        activities = Activity.query.all()
        activity = Activity.query.first()
        user = activity.user.firstname

        return render_template('dashboard.html', activities=activities, user=user)



        # token_url = "https://www.strava.com/oauth/token"
        # activities_url = "https://www.strava.com/api/v3/athlete/activities"

        # payload = {
        #     'client_id': 48415,
        #     'client_secret': 'ed4c1b2fa87eb5d3120bbb2a8a9c0f39451ca920',
        #     'refresh_token': user.strava_refresh_token,
        #     'grant_type': "refresh_token",
        #     'f': 'json'
        # }

        # print("Requesting Token...\n")
        # res = requests.post(token_url, data=payload, verify=False)
        # access_token = res.json()['access_token']
        # print("Access Token = {}\n".format(access_token))

        # header = {'Authorization': 'Bearer ' + access_token}
        # param = {'per_page': 200, 'page': 1}
        # my_dataset = requests.get(activities_url, headers=header, params=param).json()

        # print(token)
        # print("Access Token: ", token['access_token'])
        # print("Refresh Token: ", token['refresh_token'])

# # ... time passes ...
# if time.time() > client.token_expires_at:
#     refresh_response = client.refresh_access_token(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET,
#         refresh_token=client.refresh_token)
#     access_token = refresh_response['access_token']
#     refresh_token = refresh_response['refresh_token']
#     expires_at = refresh_response['expires_at']


# token_url = "https://www.strava.com/oauth/token"
# activites_url = "https://www.strava.com/api/v3/athlete/activities"

# payload = {
#     'client_id': 48415,
#     'client_secret': 'ed4c1b2fa87eb5d3120bbb2a8a9c0f39451ca920',
#     'refresh_token': user.strava_refresh_token,
#     'grant_type': "refresh_token",
#     'f': 'json'
# }

# print("Requesting Token...\n")
# res = requests.post(token_url, data=payload, verify=False)
# access_token = res.json()['access_token']
# print("Access Token = {}\n".format(access_token))

# header = {'Authorization': 'Bearer ' + access_token}
# param = {'per_page': 200, 'page': 1}
# my_dataset = requests.get(activites_url, headers=header, params=param).json()

# print(my_dataset[0]["name"])


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)