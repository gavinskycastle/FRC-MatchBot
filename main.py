import discord
import datetime
from discord import app_commands
from discord.ext import commands
from statbotics import Statbotics
from os import environ
from utils import *

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
intents = discord.Intents.all()

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
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="nextmatch")
@app_commands.describe(type = "Displays the next match the team will play in or the next match in the event", id = "The team/event number or id")
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

@bot.tree.command(name="recentmatch")
@app_commands.describe(type = "Displays the last played match for the team or in the event, as well as the match video if posted", id = "The team/event number or id")
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

@bot.tree.command(name="allmatches")
@app_commands.describe(type = "Displays all matches played by a team or in an event", id = "The team/event number or id")
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