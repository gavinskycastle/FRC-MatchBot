import discord
import datetime
from discord import app_commands
from discord.ext import commands
from statbotics import Statbotics
from os import environ
from utils import *
from tba import *

# Setting channel ids
BOT_TESTING_CHANNEL_ID = 1031012980692889615
CONEUNIST_CHANNEL_ID = 1040069639847301120
CHANNEL_ID = BOT_TESTING_CHANNEL_ID

# Get the token from the environment variables
TOKEN = environ['MATCH_BOT_DISCORD_TOKEN']

# Getting current year. By default, only matches from the current season are listed
year = int(datetime.date.today().strftime("%Y"))

# Initalize Statbotics
sb = Statbotics()

# TODO: Determine required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize our bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Runs when bot connects
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Basic ping command
# @bot.tree.command(name="ping")
# async def ping(interaction: discord.Interaction):
#     await interaction.response.send_message("Pong!")

@bot.tree.command(name="teaminfo", description="Display basic information about a team")
@app_commands.describe(team = "The team number or id")
async def team_info(interaction: discord.Interaction, team: int):
    team_object = get_team_object(team)
    tba_link = "https://www.thebluealliance.com/team/" + str(team)
    
    embed = discord.Embed(title=get_team_name(team_object), url=tba_link, description="", color=discord.Color.blue())
    embed.set_author(name="The Blue Alliance", url="https://www.thebluealliance.com", icon_url="https://raw.githubusercontent.com/the-blue-alliance/the-blue-alliance-logo/main/ios/tba-icon-Artwork.png")
    
    embed.add_field(name="Sponsors", value=team_object["name"], inline=False)
    embed.add_field(name="Location", value=get_team_location(team_object), inline=True)
    embed.add_field(name="Rookie Year", value=str(team_object["rookie_year"]), inline=True)
    
    view = discord.ui.View(timeout=None)
    for social in get_team_socials(team_object).items():
        view.add_item(discord.ui.Button(label=social[0], style=discord.ButtonStyle.link, url=social[1]))
    
    save_team_avatar(team_object, year)
    avatar_file = discord.File(AVATAR_TEMP_PATH, filename=AVATAR_TEMP_NAME)
    embed.set_thumbnail(url="attachment://"+AVATAR_TEMP_NAME)
    
    try:
        await interaction.response.send_message(file=avatar_file, embed=embed, view=view)
    except:
        await interaction.response.send_message(file=avatar_file, embed=embed)

# TODO: Add EPAs to team stats
@bot.tree.command(name="teamstats", description="Display ranking of a team and other skill-based stats for this season")
@app_commands.describe(team = "The team number or id")
async def team_stats(interaction: discord.Interaction, team: int):
    team_object = get_team_object(team)
    tba_link = "https://www.statbotics.io/team/" + str(team)
    
    embed = discord.Embed(title=get_team_name(team_object), url=tba_link, description="", color=discord.Color.red())
    embed.set_author(name="Statbotics", url="https://www.statbotics.io")
    
    stats_dict = sb.get_team_year(team=team, year=year)
    
    embed.add_field(name="Wins", value=str(stats_dict["wins"]), inline=True)
    embed.add_field(name="Losses", value=str(stats_dict["losses"]), inline=True)
    embed.add_field(name="Ties", value=str(stats_dict["ties"]), inline=True)

    embed.add_field(name="", value="", inline=False)
    
    embed.add_field(name="Auto EPA", value=str(round(stats_dict["auto_epa_end"], 1)), inline=True)
    embed.add_field(name="Teleop EPA", value=str(round(stats_dict["teleop_epa_end"], 1)), inline=True)
    embed.add_field(name="Endgame EPA", value=str(round(stats_dict["endgame_epa_end"], 1)), inline=True)
    embed.add_field(name="Total EPA", value=str(round(stats_dict["epa_end"], 1)), inline=True)
    
    embed.add_field(name="", value="", inline=False)
    
    embed.add_field(name="Global Rank", value=str(stats_dict["total_epa_rank"]) + " out of " + str(stats_dict["total_team_count"]), inline=True)
    if stats_dict["country"] != None:
        embed.add_field(name=stats_dict["country"] + " Rank", value=str(stats_dict["country_epa_rank"]) + " out of " + str(stats_dict["country_team_count"]), inline=True)
    if stats_dict["state"] != None:
        embed.add_field(name=stats_dict["state"] + " Rank", value=str(stats_dict["state_epa_rank"]) + " out of " + str(stats_dict["state_team_count"]), inline=True)
    
    save_team_avatar(team_object, year)
    avatar_file = discord.File(AVATAR_TEMP_PATH, filename=AVATAR_TEMP_NAME)
    embed.set_thumbnail(url="attachment://"+AVATAR_TEMP_NAME)
    
    await interaction.response.send_message(file=avatar_file, embed=embed)

@bot.tree.command(name="nextmatch", description="Displays the next match the team will play in or the next match in the event")
@app_commands.describe(type = "Either 'team' or 'event'", id = "The team/event number or id")
async def next_match(interaction: discord.Interaction, type: str, id: str):
    response = "`Sending...`"
    matches = get_team_or_event_matches(type, id, year)
    if matches == {}:
        response = "`Error: Must input valid team or event`"
    
    await interaction.response.send_message(response)
    
    if matches != {}:
        header = "**Next upcoming match for "
        if type == "team":
            header = header + format_team_header(int(id)) + ":**"
        if type == "event":
            header = header + "the " + format_event_header(id) + ":**"
        print_out = split_string_under_2000(get_match_table(get_next_match(matches)))
        await bot.get_channel(CHANNEL_ID).send(header)
        await bot.get_channel(CHANNEL_ID).send(code_block(print_out[0]))

@bot.tree.command(name="recentmatch", description="Displays the last played match for the team or in the event, as well as the match video if posted")
@app_commands.describe(type = "Either 'team' or 'event'", id = "The team/event number or id")
async def recent_match(interaction: discord.Interaction, type: str, id: str):
    response = "`Sending...`"
    matches = get_team_or_event_matches(type, id, year)
    if matches == {}:
        response = "`Error: Must input valid team or event`"
    
    await interaction.response.send_message(response)
    
    if matches != {}:
        header = "**Most recent match for "
        if type == "team":
            header = header + format_team_header(int(id)) + ":**"
        if type == "event":
            header = header + "the " + format_event_header(id) + ":**"
        print_out = split_string_under_2000(get_match_table(get_most_recent_match(matches)))
        await bot.get_channel(CHANNEL_ID).send(header)
        await bot.get_channel(CHANNEL_ID).send(code_block(print_out[0]))
        await bot.get_channel(CHANNEL_ID).send(get_match_video(get_most_recent_match(matches)))

@bot.tree.command(name="allmatches", description="Displays all matches played by a team or in an event")
@app_commands.describe(type = "Either 'team' or 'event'", id = "The team/event number or id")
async def all_matches(interaction: discord.Interaction, type: str, id: str):
    response = "`Sending...`"
    matches = get_team_or_event_matches(type, id, year)
    if matches == {}:
        response = "`Error: Must input valid team or event`"
    
    await interaction.response.send_message(response)
    
    if matches != {}:
        header = "**All matches for "
        if type == "team":
            header = header + format_team_header(int(id)) + ":**"
        if type == "event":
            header = header + "the " + format_event_header(id) + ":**"
        print_out = split_string_under_2000(get_match_table(matches))
        await bot.get_channel(CHANNEL_ID).send(header)
        for out in print_out:
            await bot.get_channel(CHANNEL_ID).send(code_block(out))

bot.run(TOKEN)