<!-- ![image placeholder for a screenshot from Slack](http://) -->

## Introduction

Lombardi is a rudimentary Slack bot that provides current and prior-season NFL statistics in response to structured natural language queries. The bot is built in Python using [Slackbot](https://github.com/lins05/slackbot) and leverages data from [stattleship](http://www.stattleship.com) in addition to other sources.

Currently, Lombardi will respond to [supported queries](#supported-queries) as long as he is added to a channel and invoked using @lombardi. Lombardi will also respond to queries sent to him via direct message.

This project is very much in the alpha stage. Much refactoring and optimization is needed, but it works.

## Requirements

- Python 3.0
- espnff (for ESPN fantasy football data)
- slackbot
- feedparser (for ESPN news headlines)

## Setup / Installation

- Create a Slack bot and obtain its API token
- Obtain ESPN Fantasy league information
- Obtain a Stattleship API token
- Clone this repository
- `pip install -r requirements.txt`
- Setup configurations in a `config.py` file within the lombardi directory, with format `var = '{your token here}'`:
	- Slack API Token: `apitoken`
	- ESPN S2: `espn_s2`
	- ESPN SWID: `swid`
	- ESPN League ID: `league_id`
	- ESPN League Year: `year`
	- Stattleship API Token: `stattleship_token`
- For Slackbot, there are a few additional ways to provide the Slack API token:
    - Creating an environment variable: `export SLACKBOT_API_TOKEN='<your token here>'` from a shell prompt
    - Adding `API_TOKEN = '<your token here>'` to the top of slackbot_settings.py
    - Add to `config.py` as described above.
- `python run.py`

## Supported Queries

Lombardi supports several queries "out of the box", but is very easily customizable just like any other slackbot.

Lombardi assumes a few general definitions:
* 'Season' and 'Year' are effectively interchangeable - e.g., the 2015-2016 NFL season is referred to by the year 2015. So, if you want results from January 2013 you would reference the year 2012 for that season
* Unless otherwise indicated, player names should be provided in full name format. E.g., you should use "Ben Roethlisberger" instead of "B. Roethlisberger" or something else. TODO: add more graceful error handling around invalid name entry, and more flexibilty for name entry overall.
* Unless otherwise indicated, queries are case-insensitive

The following queries are currently supported:

### NFL Headlines
- Returns the top 5 headlines from ESPN NFL

Example:
`NFL headlines`

### Reddit Headlines
- Returns the top 5 posts from /r/nfl

Example:
`Reddit headlines`

### NFL Scoreboard
- Returns the current NFL scoreboard

Example:
`NFL scoreboard`
`NFL scores`

### Season Stats {3-character NFL team ID}
- Returns season stats for the specified team

Example:
`season stats CAR`

### Fantasy Schedule {owner name}
- Returns the fantasy schedule for the specified team owner

Example:
`fantasy schedule roshan`

### Fantasy Scoreboard
- Returns the current fantasy scoreboard

Example:
`fantasy scoreboard`

### Fantasy Records
- Returns the ESPN fantasy power rankings

Example:
`fantasy records`
`fantasy rankings`


## Deployment

Slackbot handles the connection to Slack's servers using the provided API token, and includes support for reconnection after a connectivity loss, so theoretically this could be run on any internet-connected computer assuming all of the dependencies are installed.

Lombardi can be run pretty easily on Heroku. The included procfile will automatically execute `run.py` as a worker task. Note that when deploying to Heroku it's important to ensure you have at least one worker dyno running (you don't need any web dynos). Heroku's Python [deployment tutorial](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) is a great resource to get acquainted. Assuming all of the dependencies are installed, initial deployment should look something like this:
- `heroku create`
- `heroku config:set SLACKBOT_API_TOKEN=<your-slackbot-api-token>`
- `git push heroku master`
- `heroku ps:scale web=0`
- `heroku ps:scale worker=1`

Then, updates to the app can be deployed simply by running `git push heroku master` and allowing the app to restart.

## Future development / TODO

- Use [api.ai](api.ai) to improve natural language parsing by adding support for additional queries / multiple forms of syntax for the same question

Longer term, I'd like to enhance Lombardi to serve as a control center for a fantasy football league. The biggest change will be incorporating fantasy stats in addition to NFL ones.
