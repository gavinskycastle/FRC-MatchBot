import tbapy
from os import environ

TBA_KEY = environ["TBA_READ_KEY"]

tba = tbapy.TBA(TBA_KEY)

def get_team_object(team_number: int):
    team_string = "frc" + str(team_number)
    return tba.team(team_string)

def get_team_name(team: tba.team):
    return "Team " + str(team["team_number"]) + " - " + team["nickname"]

def get_team_location(team: tba.team):
    return team["city"] + ", " + team["state_prov"] + ", " + team["country"]

def get_team_socials(team: tba.team):
    team_socials = {"Website": team["website"]}
    
    for profile in tba.team_profiles(team["key"]):
        social_type = profile["type"].split("-")[0]
        social_link = "https://www." + social_type + ".com/" + profile["foreign_key"]
        social_name = social_type.title()
        social_dict = {social_name: social_link}
        team_socials.update(social_dict)
    return team_socials
