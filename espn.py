from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
from espnff import League
import json
import config
   
def initial_setup():
    # read in private league settings from config.py
    league_id = config.league_id
    year = config.year

    # credentials to let us see a private league
    espn_s2 = config.espn_s2
    swid = config.swid

    # get league info from ESPN
    league = League(league_id,year,espn_s2,swid)

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

    print('Input Owner: '+inputOwner)

    for team in teams:
        # the inputOwner is guaranteed to be lowercase, so we can compare against a lower() version of the ESPN data
        if(team.owner.split(' ')[0].lower() == inputOwner):
            chosenTeam = team

    # if we have an error creating chosenTeam then we couldn't find a match above
    try:
        response += 'Schedule for {}\n'.format(chosenTeam.team_name)
    except UnboundLocalError:
        return('Can\'t find that owner! Make sure you\'re using a first name.')
    
    for index,competitor in enumerate(chosenTeam.schedule):
        week = index + 1
        # TODO: add won / loss / tie status of each game
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

@respond_to('fantasy schedule (.*)', re.IGNORECASE)
def get_schedule(message, team_owner):
    
    print('Team Owner: {}'.format(team_owner))
    print(message._get_user_id())
    print(message.body)
    
    initial_setup()
    
    response = team_schedule(team_owner)
    
    message.reply(response)

@respond_to('fantasy scoreboard', re.IGNORECASE)
def get_scoreboard(message):
    initial_setup()
    response = format_scoreboard()

    message.reply(response)

@respond_to('fantasy records', re.IGNORECASE)
@respond_to('fantasy rankings', re.IGNORECASE)
def get_records(message):
    initial_setup()
    response = team_records()
    message.reply(response)


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

# store the league locally for easy testing later
# f = open('datastore.pckl', 'wb')
# pickle.dump(league, f)
# f.close()









