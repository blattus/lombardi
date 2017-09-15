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
    
    # obtain league from espn
    espn_s2 = config.espn_s2
    swid = config.swid

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

    scoreboard = league.scoreboard()
    teams = league.teams
    settings = league.settings
    power_rankings = league.power_rankings

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

@respond_to('schedule', re.IGNORECASE)
def get_schedule(message):
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









