import tbapy
import base64
import os

TBA_KEY = os.environ["TBA_READ_KEY"]
AVATAR_TEMP_NAME = "avatar.png"
AVATAR_TEMP_PATH = "temp/" + AVATAR_TEMP_NAME

tba = tbapy.TBA(TBA_KEY)

def get_team_object(team_number: int):
    team_string = "frc" + str(team_number)
    return tba.team(team_string)

def get_team_name(team: tba.team):
    return "Team " + str(team["team_number"]) + " - " + team["nickname"]

def get_team_location(team: tba.team):
    return team["city"] + ", " + team["state_prov"] + ", " + team["country"]

def save_team_avatar(team: tba.team, year: int):
    team_media = tba.team_media(team=team["key"], year=year)
    team_avatar_string = ""
    if team_media != []:
        for media in team_media:
            if media["type"] == "avatar":
                team_avatar_string = media["details"]["base64Image"]
    image_data = base64.b64decode(team_avatar_string)
    with open(AVATAR_TEMP_PATH, 'wb') as f:
        f.write(image_data)

def get_team_socials(team: tba.team):
    team_socials = {"Website": team["website"]}
    
    for profile in tba.team_profiles(team["key"]):
        social_type = profile["type"].split("-")[0]
        social_link = "https://www." + social_type + ".com/" + profile["foreign_key"]
        social_name = social_type.title()
        social_dict = {social_name: social_link}
        team_socials.update(social_dict)
    return team_socials

def get_event_webcasts(event: tba.event):
    webcasts = {}

    gameday_name = "Watch on Gameday"
    gameday_link = "https://thebluealliance.com/gameday/" + event["key"]
    gameday_dict = {gameday_name: gameday_link}
    webcasts.update(gameday_dict)

    i = 0
    for webcast in event["webcasts"]:
        i += 1
        if webcast["type"] == "twitch":
            webcast_name = f"Watch on Twitch ({i})"
            webcast_link = "https://www.twitch.tv/" + webcast["channel"]
            webcast_dict = {webcast_name: webcast_link}
            webcasts.update(webcast_dict)
    print(webcasts)
    return webcasts
