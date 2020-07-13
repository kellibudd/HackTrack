"""A database."""

import os
import server
import crud
import json
from model import connect_to_db, db, Team

os.system("dropdb run_app")
os.system("createdb run_app")

connect_to_db(server.app)
db.create_all()


def seed_users():

    with open("data/users.json") as f:
        user_data = json.loads(f.read())

    for user in user_data:

        firstname = user["firstname"]
        lastname = user["lastname"]
        phone = user["phone"]
        email = user["email"]
        password = user["password"]

        if "id" not in user:
            prof_pic = None
            strava_id = None
            strava_access_token = None
            strava_access_token_expir = None
            strava_refresh_token = None
        else:
            prof_pic = user["profile"]
            strava_id = user["id"]
            strava_access_token = user["access_token"]
            strava_access_token_expir = user["expires_at"]
            strava_refresh_token = user["refresh_token"]

        crud.create_user(
            firstname,
            lastname,
            phone,
            email,
            password,
            prof_pic,
            strava_id,
            strava_access_token,
            strava_access_token_expir,
            strava_refresh_token,
        )


def seed_teams():

    with open("data/teams.json") as f:
        team_data = json.loads(f.read())

    for team in team_data:

        team = Team(
            name=team["name"],
            coach_id=team["coach_id"],
            logo=team["logo"],
            team_banner_img=team["team_banner_img"],
            team_color=team["team_color"],
            activities_last_updated=team["activities_last_updated"],
        )

        db.session.add(team)
        db.session.commit()


def seed_team_members():

    with open("data/team_members.json") as f:
        team_member_data = json.loads(f.read())

    for member in team_member_data:

        user_id = member["user_id"]
        team_id = member["team_id"]
        role = member["role"]

        crud.create_team_member(user_id, team_id, role)


seed_users()
seed_teams()
seed_team_members()
