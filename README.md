# FRC-MatchBot

A discord bot to get match and event data from FRC competitions


## Installation

Install Python from the [official website](https://www.python.org/downloads)

Clone the repository and install the required dependencies:

```
  pip install -r requirements.txt
```
## Getting Started

Add the bot token under the system environment variable `MATCH_BOT_DISCORD_TOKEN`.

In Windows (replacing `TOKEN` with your token):

```
  setx MATCH_BOT_DISCORD_TOKEN TOKEN /m
```

You will also need a read key for The Blue Alliance.
Create an account and go to [this link.](https://www.thebluealliance.com/account) Under `Read API Keys`, enter any description and click `Add New Key`.
Copy the text outputted and set it as a system environment variable under `TBA_READ_KEY`.

In Windows (replacing `TOKEN` with your token):

```
  setx TBA_READ_KEY TOKEN /m
```

Now you are ready to run the bot from the main script:

```
  python main.py
```

The bot will remain active while the script is running. You can also use [Replit](https://replit.com) and [UptimeRobot](https://uptimerobot.com/) to run the bot continously.

## Commands

Currently, FRC-MatchBot supports the following commands:

`/teaminfo <team>`: Display basic information about a team

`/nextmatch <team or event> <id>`: Displays the next match the team will play in or the next match in the event

`/recentmatch <team or event> <id>`: Displays the last played match for the team or in the event, as well as the match video if posted

`/allmatches <team or event> <id>`: Displays all matches played by a team or in an event

`/ping`: Basic ping command

## License


[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

