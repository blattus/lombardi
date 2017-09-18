from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
from espnff import League
import pickle
import json
import config

def initial_setup():
    league_id = 580419
    year = 2017

    # credentials to let us see a private league
    
    # read in private league settings from config.py
    espn_s2 = config.espn_s2
    swid = config.swid

    # get league info from ESPN
    league = League(league_id,year,espn_s2,swid)

    #store the league locally for easy testing later
    f = open('datastore.pckl', 'wb')
    pickle.dump(league, f)
    f.close()

    # define some variables for convenience
    global scoreboard
    global teams
    global settings
    global power_rankings
    global userTable

    scoreboard = league.scoreboard()
    teams = league.teams
    settings = league.settings
    power_rankings = league.power_rankings
    userTable = {}

def team_records():
    response = ''
    
    for team in teams:
        response += '{} ({}-{})\n'.format(team.team_name,team.wins,team.losses)

    return response

def team_schedule(inputOwner):
    response = ''

    for team in teams:
        if(team.owner == inputOwner):
            chosenTeam = team

    for index,competitor in enumerate(chosenTeam.schedule):
        week = index + 1
        response += 'Week {}: vs {} ({}-{})\n'.format(week,competitor.team_name,competitor.wins,competitor.losses)

    return(response)

def format_scoreboard():
    response = ''

    for matchup in scoreboard:
        home_team = matchup.home_team.team_name
        away_team = matchup.away_team.team_name
        home_standing = matchup.data['teams'][0]['team']['record']['overallStanding']
        away_standing = matchup.data['teams'][1]['team']['record']['overallStanding']
        
        response += '{} ({}) vs {} ({})\n'.format(home_team, home_standing, away_team, away_standing)
        response += '{} - {}\n\n'.format(matchup.home_score, matchup.away_score)

    return(response)

def identify_user(slackUserId):
    if slackUserId in userTable:
        return userTable[slackUserId]
    else:
        return 'cannot find that user'

@respond_to('github', re.IGNORECASE)
def github(message):

    attachments = [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#36a64f",
            "pretext": "Optional text that appears above the attachment block",
            "author_name": "Bobby Tables",
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "http://flickr.com/icons/bobby.jpg",
            "title": "Slack API Documentation",
            "title_link": "https://api.slack.com/",
            "text": "Optional text that appears within the attachment",
            "fields": [
                {
                    "title": "Priority",
                    "value": "High",
                },
                {
                    "title2": "another",
                    "value": "meh",
                }
            ],
            "image_url": "http://my-website.com/path/to/image.jpg",
            "thumb_url": "https://platform.slack-edge.com/img/default_application_icon.png",
            "footer": "Slack API",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts": 123456789
        },
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#36a64f",
            "pretext": "Optional text that appears above the attachment block",
            "author_name": "Bobby Tables",
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "http://flickr.com/icons/bobby.jpg",
            "title": "Slack API Documentation",
            "title_link": "https://api.slack.com/",
            "text": "Optional text that appears within the attachment",
            "fields": [
                {
                    "title": "Priority",
                    "value": "High",
                },
                {
                    "title2": "another",
                    "value": "meh",
                }
            ],
            "image_url": "http://my-website.com/path/to/image.jpg",
            "thumb_url": "http://example.com/path/to/thumb.png",
            "footer": "Slack API",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts": 123456789
        }
    ]
    message.send_webapi('', json.dumps(attachments))


@respond_to('schedule', re.IGNORECASE)
def get_schedule(message):
    print(dir(message))
    print(message._get_user_id())
    print(message.body)
    initial_setup()
    
    response = team_schedule('Amogh K')
    
    message.reply(response)

@respond_to('scoreboard', re.IGNORECASE)
def get_scoreboard(message):
    initial_setup()
    response = format_scoreboard()

    message.reply(response)

@respond_to('records', re.IGNORECASE)
def get_records(message):
    initial_setup()
    response = team_records()
    message.reply(response)

# initial_setup()

# # load the content from the pickle
# f = open('datastore.pckl', 'rb')
# league = pickle.load(f)
# f.close()

# scoreboard = league.scoreboard()
# teams = league.teams
# settings = league.settings
# power_rankings = league.power_rankings
# team1 = league.teams[0]

# # print(scoreboard[1].__dict__)
# format_scoreboard()









