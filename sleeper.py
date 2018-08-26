from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import requests
import config
import sqlite3
import random
import time
import json

league_id = config.sleeper_league_id
sleeper_owner_map = config.sleeper_owner_map

def rosters():
	''' 
	provides rosters 
	'''
	
	# connect to database
	conn = sqlite3.connect('sleeper.db')
	db = conn.cursor()

	# get roster results from sleeper API
	r = requests.get('https://api.sleeper.app/v1/league/{}/rosters'.format(league_id))
	results = r.json()
	
	for sleeper_team in results:
		owner_id = sleeper_team['owner_id']
		sleeper_team_name = sleeper_owner_map[owner_id]['sleeper_team_name']

		unformatted_roster = sleeper_team['starters']
		
		# format the roster by translating player IDs to names
		query_result = db.execute('''SELECT fantasy_positions, first_name, last_name, team
								FROM players
								WHERE player_id IN (?,?,?,?,?,?,?,?,?)
								ORDER BY fantasy_positions''', unformatted_roster)
		

		for row in query_result:
			# print('{} - {} {} ({})'.format(row[0],row[1],row[2],row[3]))
			pass

	# commit and close
	conn.commit()
	conn.close()

	return

def who_owns(first_name,last_name):
	''' 
	allows a slack user to ask who owns a specific fantasy player
	'''

	search_string = [first_name,last_name]

	# connect to database
	conn = sqlite3.connect('sleeper.db')
	db = conn.cursor()

	query_result = db.execute('''SELECT player_id
								FROM players
								WHERE first_name LIKE ?
								AND last_name LIKE ?''',search_string)
	row = query_result.fetchone()

	# check for no results
	if row is None:
		return('Could not find that player')
	else:
		player_id = row[0]
		owner_id = None

		# query sleeper API for rosters
		r = requests.get('https://api.sleeper.app/v1/league/{}/rosters'.format(league_id))
		results = r.json()

		for sleeper_team in results:

			# get list of players on the team
			players_on_team = sleeper_team['players']

			# check if the searched-for player is on the team. If yes, grab the sleeper owner ID
			if player_id in players_on_team:
				owner_id = sleeper_team['owner_id']

		# map the owner ID to the username
		if owner_id is None:
			return('Nobody! They\'re available!')
		else:
			sleeper_team_name = sleeper_owner_map[owner_id]['sleeper_team_name']
			return(sleeper_team_name)

def waiver_positions():
	''' 
	generates a report of waiver priority
	'''
	r = requests.get('https://api.sleeper.app/v1/league/{}/rosters'.format(league_id))
	results = r.json()

	# make a dummy waivers list then update each element with the position in that spot
	# hardcoded to 12 spots for my league
	waiver_order = [1,2,3,4,5,6,7,8,9,10,11,12]
	for sleeper_team in results:
		owner_id = sleeper_team['owner_id']
		team_name = sleeper_owner_map[owner_id]['sleeper_team_name']
		waiver_order[sleeper_team['settings']['waiver_position'] - 1] = team_name
	
	return(waiver_order)

# @respond_to('League Rosters', re.IGNORECASE)
def get_team_stats(message, team):
	response = rosters(team)
	message.reply(response)

@respond_to('who owns (.*) (.*)',re.IGNORECASE)
@respond_to('who has (.*) (.*)',re.IGNORECASE)
def get_who_owns(message,first_name,last_name):
	result = who_owns(first_name,last_name)

	repsonse_prefix_list = ['That would be','It\'s','The team with that player is','Looks like','Yep,']

	response = ''
	if result is 'Could not find that player':
		response = result
	else:	
		response = '{} {}'.format(random.choice(repsonse_prefix_list),result)

	attachments = [
		{
		"fallback": "Player Lookup",
		"color": "#00c852",
		"author_name": "Punt You Fools",
		"author_link": "https://sleeper.app/leagues/326582399653662720",
		"author_icon": "https://sleeper.app/favicon.ico",
		"title": "Player Lookup -- {} {}".format(first_name,last_name),
		"title_link": "https://sleeper.app/leagues/326582399653662720",
		"text": response,
		"footer": "Data from Sleeper API",
		"ts": time.time()
		}
	]
	
	message.send_webapi('',json.dumps(attachments))



@respond_to('Waiver Positions',re.IGNORECASE)
def get_waiver_positions(message):
	waiver_list = waiver_positions()
	emoji_list = [':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:',':keycap_ten:',':clock11:',':poop:']

	response = ''
	for i in range(12):
		response += '{} {}\n'.format(emoji_list[i],waiver_list[i])

	attachments = [
		{
		"fallback": "Waiver Position Report",
		"color": "#00c852",
		"author_name": "Punt You Fools",
		"author_link": "https://sleeper.app/leagues/326582399653662720",
		"author_icon": "https://sleeper.app/favicon.ico",
		"title": "Waiver Position Report",
		"title_link": "https://sleeper.app/leagues/326582399653662720",
		"text": response,
		"footer": "Data from Sleeper API",
		"ts": time.time()
		}
	]
	
	message.send_webapi('',json.dumps(attachments))



