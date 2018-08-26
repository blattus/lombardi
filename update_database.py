import json
import sqlite3

f = open('sleeper_players.json')
player_file = json.loads(f.read())

def init_db():
	''' 
	initializes the database with a 'players' table
	'''
	conn = sqlite3.connect('sleeper.db')
	db = conn.cursor()

	db.execute('''CREATE TABLE players
			(player_id text, hashtag text, depth_chart_position real, status text, sport text, fantasy_positions text, 
			number real, search_last_name text, injury_start_date text, weight text, position text, practice_participation text,
			sportradar_id text, team text, last_name text, college text, fantasy_data_id real, injury_status text, height text,
			search_full_name text, age real, stats_id text, birth_country text, espn_id text, search_rank real, first_name text,
			depth_chart_order real, years_exp real, rotowire_id text, rotoworld_id real, search_first_name text, yahoo_id text)''')

	conn.commit()
	conn.close()


def update_db():

	# connect to db
	conn = sqlite3.connect('sleeper.db')
	db = conn.cursor()

	# we can assume we're working with fresh data, so start by dropping the table


	# format the data and insert
	for key in player_file:
		p = player_file[key]
		temp_player_data = [p['player_id'],p['hashtag'],p['depth_chart_position'],p['status'],p['sport'],
			str(p['fantasy_positions']),p['number'],p['search_last_name'],p['injury_start_date'],p['weight'],
			p['position'],p['practice_participation'],p['sportradar_id'],p['team'],p['last_name'],
			p['college'],p['fantasy_data_id'],p['injury_status'],p['height'],p['search_full_name'],
			p['age'],p['stats_id'],p['birth_country'],p['espn_id'],p['search_rank'],p['first_name'],
			p['depth_chart_order'],p['years_exp'],p['rotowire_id'],p['rotoworld_id'],p['search_first_name'],p['yahoo_id']]

		db.execute('INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', temp_player_data)

	# commit and close
	conn.commit()
	conn.close()

