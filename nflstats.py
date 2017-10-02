from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
from stattleship import *
import config

query = Stattleship()

token = query.set_token(config.stattleship_token)

def weekly_schedule():
	response = ''
	week = 4

	# TODO: dynamically calculate the week
	output = query.ss_get_results(sport='football', league='nfl', ep='games', week=week)
	games = output[0]['games']

	# it looks like all games in the response have the same updated timestamp, so let's take the first one
	updated_at = output[0]['games'][0]['updated_at']

	response += 'Scores for Week {} of the NFL\n'.format(week)
	response += 'Updated at: {}\n\n'.format(updated_at)

	for game in games:
		response += '{scoreline} ({clock})\n'.format(scoreline=game['scoreline'],clock=game['clock'])

	return response

def team_stats(team):
	output = query.ss_get_results(sport='football', league='nfl', ep='team_season_stats', team_id=team)
	
	# the team_season_stats endpoint returns 3 days worth of calculated stats. We should pick the first / most recent one
	stats = output[0]['team_season_stats'][0]
	teams = output[0]['teams'][0]

	# define a convenience name + nickname variable
	name = teams['name']+' '+teams['nickname']

	# set any "None" variables to 0 for easy addition later on
	for stat in stats:
		if(stats[stat] is None):
			stats[stat] = 0

	response = ''
	response += 'Season Stats for the {}\n'.format(name)
	response += 'Updated at {}\n'.format(stats['updated_at'])
	response += 'Total 1st Downs: {}\n'.format(stats['first_downs'])
	response += '1st Downs (rush-pass-penalty: {}-{}-{}\n'.format(stats['rush_first_downs'],stats['pass_first_downs'],stats['penalty_first_downs'])
	response += '3rd Down Conversions: {}/{}\n'.format(stats['third_down_conversions'],stats['third_down_attempts'])
	response += '4th Down Conversions: {}/{}\n'.format(stats['fourth_down_attempts'],stats['fourth_down_conversions'])
	response += 'Total Offensive Yards: {}\n'.format(stats['rush_yards'] + stats['pass_yards'])
	# TODO: calculate total plays and average yards per play for all offense
	response += 'Total Rushing Yards: {}\n'.format(stats['rush_yards'])
	response += 'Rushing (plays - avg yards): {}\n'.format(stats['rush_attempts'],stats['rush_avg'])
	response += 'Total Passing Yards: {}\n'.format(stats['pass_yards'])
	response += 'Passing (comp - att - int - avg): {}-{}-{}-{}\n'.format(stats['pass_completions'],stats['pass_attempts'],stats['pass_interceptions'],stats['pass_avg_yards'])
	response += 'Sacks: {}\n'.format(stats['defense_sacks'])
	response += 'Field Goals: {} / {} (long: {})\n'.format(stats['field_goal_made'], stats['field_goal_attempts'], stats['field_goal_longest_yards'])
	response += 'Touchdowns: {}\n'.format(stats['rush_touchdowns'] + stats['pass_touchdowns'] + stats['punt_return_touchdowns'] + stats['kick_return_touchdowns'] + stats['defense_interceptions_touchdowns'] + stats['defense_fumble_touchdowns'])
	response += 'Touchdowns (rush - pass - ret - def): {}-{}-{}-{}\n'.format(stats['rush_touchdowns'],stats['pass_touchdowns'],stats['punt_return_touchdowns']+stats['kick_return_touchdowns'],stats['defense_fumble_touchdowns']+stats['defense_interceptions_touchdowns'])

	return response

@respond_to('NFL scores', re.IGNORECASE)
@respond_to('NFL scoreboard', re.IGNORECASE)
def get_weekly_schedule(message):
    response = weekly_schedule()
    message.reply(response)

@respond_to('Season Stats (.*)', re.IGNORECASE)
def get_team_stats(message, team):
	team = 'nfl-'+team
	response = team_stats(team)
	message.reply(response)


