<!-- ![image placeholder for a screenshot from Slack](http://) -->

## Introduction

Lombardi is a rudimentary Slack bot that provides current and prior-season NFL statistics in response to structured natural language queries. The bot is built in Python using [Slackbot](https://github.com/lins05/slackbot) and leverages data from the [nflgame](https://github.com/BurntSushi/nflgame) API in addition to other sources.

Currently, Lombardi will respond to [supported queries](#supported-queries) as long as he is added to a channel and invoked using @lombardi. Lombardi will also respond to queries sent to him via direct message. 

This project is very much in the alpha stage. Much refactoring and optimization is needed, but it works. 

## Requirements

- Python 2.6 or 2.7 (may work in Python 3 but at your own risk)
- nflgame
- slackbot
- feedparser (for ESPN news headlines)

## Installation

- Create a Slack bot and obtain its API token
- Clone this repository
- `pip install -r requirements.txt`
- Provide your API token to the application by either:
    - Creating an environment variable: `export SLACKBOT_API_TOKEN='<your token here>'` from a shell prompt
    - Adding `API_TOKEN = '<your token here>'` to the top of slackbot_settings.py
    - Creating a config.py file in the lombardi directory with apitoken = '<your token here>'
- `python run.py`

## Supported Queries

Lombardi supports several queries "out of the box", but is very easily customizable just like [any other slackbot](link to other slackbots). 

Lombardi generally follows the conventions of nflgame and slackbot. This means that a few definitions apply across the board:
* 'Season' and 'Year' are effectively interchangeable - e.g., the 2015-2016 NFL season is referred to by the year 2015. So, if you want results from January 2013 you would reference the year 2012 for that season
* Unless otherwise indicated, player names should be provided in full name format. E.g., you should use "Ben Roethlisberger" instead of "B. Roethlisberger" or something else. There is currently an [issue open](#issuelink) to add more graceful error handling around invalid name entry, and more flexibilty for name entry overall.
* Unless otherwise indicated, queries are case-insensitive

The following queries are currently supported:

### Top [position] [year]
- Returns statistics for the top 5 players of the provided position in the provided season

Example:
`Top RB 2015`

### Player Stats for [player name] in [year] [optional: 'detailed']
- Returns aggregate stats for a given player in a given season. Relevant stats are shown based on the player's position. If 'detailed' is included, week-by-week stats are shown.

Example:
`player stats for Ben Roethlisberger in 2015`
`asdfasdf`

`player stats for Ben Roethlisberger in 2015 detailed`
`asdf
asdf
asdf
fads`

### Bio [player name]
- Returns player biographical information, including team, position, team, college, height/weight, years pro, and a link to the player's profile on NFL.com
- Player name must be provided as a full name, e.g., "Tom Brady" or "Antonio Gates"

Example:
`bio Antonio Gates`

````
Name: Antonio Gates
Position:*​ TE
​Team: SD
​College:​ Kent State
​Ht/Wt: 6' 4", 255lbs
​Yrs Pro:​ 13
​Profile URL:​ http://www.nfl.com/player/antoniogates/2505299/profile
````

### Game stats [year] [week] [team]
- Returns a detailed game summary for the specified game. The summary includes:
- Aggregate game statistics (score, first downs, yardages, penalty / turnover stats, punt stats, and TOP)
- A scoring summary
- Team name must be provided in abbreviated format (e.g., "CAR" or "JAC")

Example:
`Forthcoming....`

### NFL Headlines
- Returns the top 5 headlines from ESPN NFL

Example:
`Forthcoming`

### Reddit Headlines
- Returns the top 5 posts from /r/nfl

Example:
`Forthcoming`


## Deployment

Slackbot handles the connection to Slack's servers using the provided API token, and includes support for reconnection after a connectivity loss, so theoretically this could be run on any internet-connected computer assuming all of the dependencies are installed.

I'm working on getting this running on Heroku...instructions for that will go here soon.

## Future development / TODO

- Switch to using [nfldb](https://github.com/BurntSushi/nfldb) or [Stattleship's API](https://www.stattleship.com) to improve query response time (which can be very long for full-season queries)
- Use [api.ai](api.ai) to improve natural language parsing by adding support for additional queries / multiple forms of syntax for the same question

Longer term, I'd like to enhance Lombardi to serve as a control center for a fantasy football league. The biggest change will be incorporating fantasy stats in addition to NFL ones. 

