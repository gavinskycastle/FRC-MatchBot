from statbotics import Statbotics
from prettytable import PrettyTable
from datetime import datetime

sb = Statbotics()

def get_most_recent_match(matches: list):
    recent_match = {}
    for match in matches[::-1]:
        if match["status"] == "Completed":
            recent_match = match
            break
    return recent_match

def get_next_match(matches: list):
    next_match = {}
    for match in matches:
        if match["status"] != "Completed":
            next_match = match
            break
    return next_match

def get_match_name(match: dict):
    semifinal = False
    if match["comp_level"] == "qm":
        match_name = "Qualification "
    elif match["comp_level"] == "qf":
        match_name = "Quarterfinal "
    elif match["comp_level"] == "sf":
        match_name = "Semifinal "
        semifinal = True
    elif match["comp_level"] == "f":
        match_name = "Final "
    else:
        match_name = ""
    
    if semifinal:
        match_name = match_name + str(match["set_number"]) + " Match "
    match_name = match_name + str(match["match_number"])
    
    return match_name

def add_match_to_table(match: dict, table):
    try:
        match_event_name = sb.get_event(event=match["event"])["name"]
        match_name = get_match_name(match)
        
        red_score = match["red_score"]
        blue_score = match["blue_score"]
        winner = match["winner"].title()
        
        if red_score == -1 or blue_score == -1:
            red_score = "TBD"
            blue_score = "TBD"
            winner = "TBD"
        
        table.add_row([match_event_name, match_name, match["red_1"], match["red_2"], match["red_3"], match["blue_1"], match["blue_2"], match["blue_3"], red_score, blue_score, winner])
    except KeyError:
        table.add_row(["TBD", "TBD", "TBD", "TBD", "TBD", "TBD", "TBD", "TBD", "TBD", "TBD", "TBD"])

def get_match_table(matches):
    table = PrettyTable()
    table.field_names = ["Event", "Match", "Red 1", "Red 2", "Red 3", "Blue 1", "Blue 2", "Blue 3", "Red Score", "Blue Score", "Winner"]
    if type(matches) is list:
        for match in matches:
            add_match_to_table(match, table)
    elif type(matches) is dict:
        add_match_to_table(matches, table)
    return table.get_string()

def code_block(string):
    return "```"+string+"```"

def get_team_or_event_matches(type, id, year):
    if type == "team":
        try:
            return sb.get_matches(team=int(id), year=year)
        except Exception:
            return {}
    elif type == "event":
        try:
            return sb.get_matches(event=id)
        except Exception:
            return {}
    else:
        return {}

# If a string is too long to be outputted as one message, split it into strings such that it never reaches the 2000 character limit.
def split_string_under_2000(string):
    lines = string.splitlines()
    split_strings = []
    split_string = ""
    for line in lines:
        if len(split_string) > 1800:
            split_strings.append(split_string)
            split_string = ""
        split_string = split_string + line + "\n"
    split_strings.append(split_string)
    return split_strings

def format_team_header(team: int):
    team_name = sb.get_team(team=team)["name"]
    return f"Team {str(team)} ({team_name})"

def format_event_header(event: str):
    event_name = sb.get_event(event=event)["name"]
    return event_name

def get_match_video(match: str):
    try:
        return "https://www.youtu.be/" + match["video"]
    except KeyError:
        return ""

# Written by ChatGPT
def date_range_string(start_date: str, end_date: str) -> str:
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Extract the month and day information
    start_month = start_dt.strftime('%B')
    end_month = end_dt.strftime('%B')
    start_day = str(int(start_dt.strftime('%d')))
    end_day = str(int(end_dt.strftime('%d')))
    
    # Check if the start and end dates are in the same month
    if start_month == end_month:
        return f"{start_month} {start_day} to {end_day}"
    else:
        return f"{start_month} {start_day} to {end_month} {end_day}"