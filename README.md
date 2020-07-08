# HackTrack

>HackTrack provides teams with a single platform for analyzing running data, sharing real-time feedback, accessing performance metrics, and navigating training history. The inspiration for this project stems from my experience as distance runner at a Division I program, where I manually tracked my workouts and mileage in a training diary. The applica


### Technologies
  - Tech Stack: Python, JavaScript, HTML, CSS, Flask, Jinja, jQuery, AJAX, PostgreSQL, SQLAlchemy, Bootstrap, Stravalib 
  - APIs: Strava REST API
### Features
  - New user registration using OAuth2.0
  - Automated ingestion of Strava running activity
  - User functionality to:
    - Join and create teams
    - View weekly mileage and performance metrics in team dashboard
    - Access historical training data
    - Leave messages on activities
    - View message history
    - Login and Logout

#### Register as a new user
![registration](https://github.com/kellibudd/hacktrack/blob/master/static/img/registration.gif)
#### View team activities and detailed metrics
![dashboard](https://github.com/kellibudd/hacktrack/blob/master/static/img/view_activities.gif)
#### Access historical training data
![history](https://github.com/kellibudd/hacktrack/blob/master/static/img/navigate_weeks.gif)
#### Leave comments on activities and view message history
![comments](https://github.com/kellibudd/hacktrack/blob/master/static/img/comments.gif)






### Installation
#### Prerequisites
  - Python3
  - PostgreSQL
  - Client ID and Client Secret from Strava -> https://www.strava.com/settings/api

#### Clone or fork repository
```sh
$ git clone https://github.com/kellibudd/HackTrack.git
```
#### Create and activate a virtual environment in your HackTrack directory
```sh
$ virtualenv
$ source env/bin/activate
```
#### Install requirements
```sh
$ pip3 install -r requirements.txt
```
#### Create a secrets.sh file to store all sensitive keys
  - Flask app secret key
  - Client ID and Client Secret supplied by Strava

#### Activate secrets in virtual environment
```sh
$ source secrets.sh
```
#### Run the server
```sh
$ python3 server.py
```

### About the Engineer

Prior to attending Hackbright Academy’s 12-week immersive full-stack software engineering program, Kelli held several roles in Accounting and Audit. Her curiosity, persistence, and analytical approach to problem solving made her highly effective as an Accountant but she struggled to feel fulfilled by the cyclical nature of the role. In 2018, she moved halfway across the country to take a job with Instacart in San Francisco. This shift to a growing technology start-up solidified her interest in Software Engineering and ultimately led her to pursue the Fellowship program at Hackbright. She is eager to use her platform to build impactful products and encourage other women to view this as an attainable and inclusive career path.

### Acknowledgments

Thank you to my mentors, classmates, and advisors for the endless support and guidance.




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [registration]: <https://github.com/kellibudd/hacktrack/blob/master/static/img/registration.gif>
   [dashboard]: <https://github.com/kellibudd/hacktrack/blob/master/static/img/view_activities.gif>
   [history]: <https://github.com/kellibudd/hacktrack/blob/master/static/img/navigate_weeks.gif>
   [comments]: <https://github.com/kellibudd/hacktrack/blob/master/static/img/comments.gif>
