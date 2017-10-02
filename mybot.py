from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
#import nflgame
import feedparser

@respond_to('hi', re.IGNORECASE)
@respond_to('hello', re.IGNORECASE)
@respond_to('what\'s up', re.IGNORECASE)
def hi(message):
	message.reply('Yo. For a list of available comamands say `@lombardi help` or just `help` if this is a DM')
	## react with thumbs up emoji
	# message.react('+1')
	# TODO: add some personalization - the message object contains data on who the sender is. I think this will work:
	# sender = "@" + message.channel._client.users[message.body['user']][u'name']

@respond_to('help', re.IGNORECASE)
def help(message):
	# TODO: either use the built-in slackbot argument finder, or export this into a separate function for refactor
	response = 'Hi! I can respond to the following commands:\n'
	#response += '* `top [position] [year]`\n'
	#response += '* `simple player stats [full name] [year]`\n'
	#response += '* `detailed player stats [full name] [year]`\n'
	#response += '* `Game stats [year] [week] [team]`\n\n'
	#response += '* `bio [full name]`\n'
	response += '* `Reddit headlines`\n'
	response += '* `ESPN headlines`\n'
	response += '* `team headlines [team abbreviation]`\n'
	response += 'scoreboard (provides the current week\'s fantasy scoreboard'
	response += 'schedule [owner name] - provides the specified owner\'s fantasy schedule'
	response += 'I\'m always learning new things! If there\'s something you\'d like to see either '
	response += 'ask my creator or check out my documentation on GitHub (https://github.com/blattus/lombardi) and add it yourself!\n'
	response += ''

	message.reply(response)

# @respond_to('nfl', re.IGNORECASE)
# def nfl(message):
# 	games = nflgame.games(2013, week=1)
# 	players = nflgame.combine_game_stats(games)
# 	response = ''
# 	for p in players.rushing().sort('rushing_yds').limit(5):
# 	    msg = '%s %d carries for %d yards and %d TDs\n' % (p, p.rushing_att, p.rushing_yds, p.rushing_tds)
# 	    response += msg
# 	message.reply(response)

# stats for top players at a given position in a given season
#@respond_to('top$', re.IGNORECASE)
#@respond_to('top (.*) (.*)', re.IGNORECASE)
def top(message, pos_abbreviation, year): # in this definition, message is the object, and position and year are passed to the function!

	# convert year into an int
	year = int(year)

	# if the position provided is not a position, then respond saying so
	if pos_abbreviation not in ['QB','RB','WR','K']:
		# TODO: move positions into an include like valid_positions to futureproof if more positions are added
		message.reply('You didn\'t give me a valid position! Please use QB, RB, WR, or K (TE support coming soon!)')
		return

	# same story if the year is invalid
	# TODO: make year range auto calculated based on current time
	if year not in range(2009,2017):
		message.reply('You didn\'t give me a valid year! I only have data from 2009 - 2016')
		return

	# calculate the game stats using nflgame
	games = nflgame.games(year)
	players = nflgame.combine_game_stats(games)

	# intiialize response variable
	response = 'Here are the stats for the top 5 %s in %s:\n' % (pos_abbreviation, year)

	# TODO: refactor the crap out of this mess (probably move the positions into a lookup array)
	# TODO: figure out how to add defense stats (may have to sum across all DEF players)
	# TODO (more urgent) add TE
	if pos_abbreviation == 'QB':
		for p in players.passing().sort('passing_yds').limit(5):
			msg = '*%s:* %d passes for %d yards and %d TDs\n' % (p, p.passing_att, p.passing_yds, p.passing_tds)
			response += msg
	if pos_abbreviation == 'RB':
		for p in players.rushing().sort('rushing_yds').limit(5):
			yards_per_carry = int(float(p.rushing_yds) / float(p.rushing_att))
			msg = '*%s:* %d rushes for %d yards (%d YPC) and %d TDs\n' % (p, p.rushing_att, p.rushing_yds, yards_per_carry, p.rushing_tds)
			response += msg
	if pos_abbreviation == 'WR':
		for p in players.receiving().sort('receiving_yds').limit(5):
			msg = '*%s*: %d receptions for %d yards and %d TDs\n' % (p, p.receiving_rec, p.receiving_yds, p.receiving_tds)
			response += msg
	if pos_abbreviation == 'K':
		for p in players.kicking().sort('kicking_yds').limit(5):
			msg = '*%s:* %d FG out of %d attempts and %d total XP\n' % (p, p.kicking_fgm, p.kicking_fga, p.kicking_xpmade)
			response += msg

	message.reply(response)

# simple stats for a given player in a given season
#@respond_to('simple player stats (.*\s.*) (.*)', re.IGNORECASE)
#@respond_to('simplified player stats (.*\s.*) (.*)', re.IGNORECASE)
def simpleplayerstats(message, player, year):
	year = int(year)
	response = 'Here are the stats for %s in %s:\n' % (player, year)

	# calculate games and players variables
	games = nflgame.games(year)
	players = nflgame.combine(games)

	# find the specific player from the combined game data:
	try:
		result = nflgame.find(player)[0]
	except IndexError:
		message.reply('Could not find that player. Maybe check the spelling and try again?')

	# for whole-season data we can just get the player from the combined game data versus iterating through each game
	myplayer = players.name(result.gsis_name)

	# For some players there is no gsis_name....probably a way to work around this but for now throw an error
	if myplayer is None:
		message.reply('Something strange happened. I may not have data for that player')

	if myplayer.player.position == 'QB':
		response += '%d total passing yds, %d total passing TD in %d' % (myplayer.passing_yds, myplayer.passing_tds, year)
	if myplayer.player.position in ('WR','TE'):
		response += '%d total receiving yds, %d total receiving TD in %d' % (myplayer.receiving_yds, myplayer.receiving_tds, year)
	if myplayer.player.position == 'RB':
		response += '%d total rushing yds, %d total rushing TD in %d' % (myplayer.rushing_yds, myplayer.rushing_tds, year)

	message.reply(response)

# detailed stats for a given player in a given season
#@respond_to('detailed player stats (.*\s.*) (.*)', re.IGNORECASE)
def detailedplayerstats(message, player, year):
	year = int(year)
	response = 'Here are the stats for %s in %s:\n' % (player, year)

	# calculate games and players variables
	games = nflgame.games(year)
	players = nflgame.combine(games)

	# find the specific player from the combined game data:
	try:
		result = nflgame.find(player)[0]
	except IndexError:
		message.reply('Could not find that player. Maybe check the spelling and try again?')

	# this works to calculate games but specifying the team is MUCH faster:
	# #games = nflgame.games(year, home="PIT", away="PIT")
	#games = nflgame.games(year)

	# initialize
	total_yds = 0
	total_tds = 0

	# iterate through all games in the season (calculated above)
	for game in games:
		# for each game in the season, we only want data for the player being queried:
		myplayer = game.players.name(result.gsis_name)

		if game.players.name(result.gsis_name):
	        # could test by using if 'passing_yds' in myplayer.__dict__, but this seems more straightforward for now?
			try:
				passing_yds = myplayer.passing_yds
			except NameError:
			    passing_yds = '0'
			try:
			    passing_tds = myplayer.passing_tds
			except NameError:
			    passing_tds = '0'
			try:
			    receiving_yds = myplayer.receiving_yds
			except NameError:
			    receiving_yds = '0'
			try:
			    receiving_tds = myplayer.receiving_tds
			except NameError:
			    receiving_tds = '0'
			try:
			    rushing_yds = myplayer.rushing_yds
			except NameError:
			    rushing_yds = '0'
			try:
			    rushing_tds = myplayer.rushing_tds
			except NameError:
			    rushing_tds = '0'

			if myplayer.player.position == 'QB':
			    response += '*Week {:2}* - {:3} passing yds, {:2} passing TD\n'.format(game.schedule['week'], passing_yds, passing_tds)
			    total_yds += passing_yds
			    total_tds += passing_tds
			if myplayer.player.position == 'WR':
			    response += '*Week {:2}* - {:3} receiving yds, {:2} receiving TD\n'.format(game.schedule['week'], receiving_yds, receiving_tds)
			    total_yds += receiving_yds
			    total_tds += receiving_tds
			if myplayer.player.position == 'RB':
			    response += '*Week {:2}* - {:3} rushing yds, {:2} rushing TD\n'.format(game.schedule['week'], rushing_yds, rushing_tds)
			    total_yds += rushing_yds
			    total_tds += rushing_tds
			if myplayer.player.position == 'TE':
			    response += '*Week {:2}* - {:3} receiving yds, {:2} receiving TD\n'.format(game.schedule['week'], receiving_yds, receiving_tds)
			    total_yds += receiving_yds
			    total_tds += receiving_tds

	# hyphens for separation
	response += '-'*30

	# Season summary
	response += '\n*{:4} Season - {:4} yds, {:2} TD*'.format(year, total_yds, total_tds)

	message.reply(response)

#@respond_to('bio $', re.IGNORECASE)
#@respond_to('bio (.*)', re.IGNORECASE)
def playerbio(message, player):
	response = 'Here\'s the bio for %s:\n' % player
	bigben = nflgame.find(player)[0]
	height_in_feet = '%d\' %d\"' % (int(bigben.height)/12, int(bigben.height)%12)
	response += '*Name:* %s\n*Team:* %s\n*Position:* %s\n*College:* %s\n' % (bigben.full_name, bigben.team, bigben.position, bigben.college)
	response += '*Ht/Wt:* %s, %dlbs\n*Yrs Pro:* %d\n*Profile URL:* %s' % (height_in_feet, bigben.weight, bigben.years_pro, bigben.profile_url)

	message.reply(response)

@respond_to('ESPN Headlines', re.IGNORECASE)
def espnheadlines(message):
	d = feedparser.parse('http://espn.go.com/espn/rss/nfl/news')

	response = 'Here are the Top 5 NFL Headlines from ESPN:\n'

	for x in range(0,5):
		try:
			title = d['items'][x]['title']
			link = d['items'][x]['links'][0]['href']

			response += '*%s*:\n%s\n' % (title, link)

		except:
			"Uhhh having trouble connecting. Try again in a bit."

	message.send(response)

@respond_to('Reddit Headlines', re.IGNORECASE)
def redditheadlines(message):
	d = feedparser.parse('https://www.reddit.com/r/nfl/.rss')

	response = 'Here are the Top 5 NFL Headlines from /r/nfl on Reddit:\n'

	for x in range(0,5):
		try:
			title = d['items'][x]['title']
			link = d['items'][x]['links'][0]['href']

			response += '*%s*:\n%s\n' % (title, link)

		except:
			"Uhhh having trouble connecting. Try again in a bit."

	message.send(response)

@respond_to('Team Headlines (.*)', re.IGNORECASE)
def team_headlines(message, team):
	# NFL provides team-specific RSS feeds with simple URI handling
	# From http://www.nfl.com/rss/rsslanding
	query_url = 'http://www.nfl.com/rss/rsslanding?searchString=team&abbr={}'.format(team.upper())

	d = feedparser.parse(query_url)

	# Handle invalid teams by checking the result page for a team-specific description
	if d['feed']['subtitle'] == 'No Description':
		message.reply('Invalid team! Make sure you\'re using a valid 3-letter NFL Team abbreviation.')

	else:
		response = d['feed']['subtitle']+':\n'

		for x in range(0,5):
		    try:
		        title = d['items'][x]['title']
		        link = d['items'][x]['links'][0]['href']

		        response += '*%s*:\n%s\n' % (title, link)

		    except:
		        "Uhhh having trouble connecting. Try again in a bit."

		message.reply(response)

#@respond_to('game stats (.*) (.*) (.*)', re.IGNORECASE)
def get_game_stats(message, year, week, team):
	year = int(year)
	week = int(week)

	# nflgame requrires team abbreviations are uppercase
	game = nflgame.one(year,week=week,home=team.upper(),away=team.upper())

	# TODO: build actual validation for the year, week, team and improve the error reporting
	if game is None:
		message.reply("Yeah...I didn't find that game. Try again?")
		return

	# format the scoring summary
	scoring_summary = ''
	for x in game.scores:
		scoring_summary += x+'\n'

	# initialize the response
	response = 'Stats for %s\n(in week %d of the %d season):\n' % (game, week, year)

	# TODO: refactor the crap out of this when my eyes aren't closing against my will:
	stats_list = [
	'First Downs:',
	'Total Yards:',
	'Passing Yards:',
	'Rushing Yards:',
	'Penalties:',
	'Penalty Yards:',
	'Turnovers:',
	'Punts:',
	'Punt Yards:',
	'Punt Average:',
	'Possession Time:']

	# add game stats to the response
	for x in range(0,11):
		response += '%s %s - %s\n' % (stats_list[x], game.stats_away[x], game.stats_home[x])

	# add scoring summary to the response
	response += '\nScoring Summary:\n%s' % scoring_summary

	message.reply(response)

