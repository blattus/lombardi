from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import nflgame
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

@listen_to('Can I get some stats in here?')
def chief(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('Tell me what you want, chief')

@respond_to('help', re.IGNORECASE)
def help(message):
	# TODO: either use the built-in slackbot argument finder, or export this into a separate function for refactor
	response = 'Hi! I can respond to the following commands:\n'
	response += '* `top [position] [year]`\n'
	response += '* `player stats [full name] [year] [\'detailed\' (optional)]`\n'
	response += '* `Game stats [year] [week] [team]`\n\n'
	response += '* `bio [full name]`\n'
	response += '* `Reddit headlines`\n'
	response += '* `ESPN headlines`\n'
	response += 'I\'m always learning new things! If there\'s something you\'d like to see either '
	response += 'ask my creator or check out my documentation and add it yourself!\n'
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
@respond_to('top (.*) (.*)', re.IGNORECASE)
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
	if year not in range(2009,2016):
		message.reply('You didn\'t give me a valid year! I only have data from 2009 - 2015')
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

# stats for a given player in a given season
#@respond_to('player stats $', re.IGNORECASE)
@respond_to('player stats (.*\s.*) (.*)', re.IGNORECASE)
# @respond_to('player stats (.*\s.*) (.*) (.*)', re.IGNORECASE)
# @respond_to('player stats (?:.*) (.*\s.*) (?:.*) (.*) (.*)', re.IGNORECASE)
def playerstats(message, player, year, details='no'):
	year = int(year)
	response = 'Here are the stats for %s in %s:\n' % (player, year)

	# calculate games and players variables
	games = nflgame.games(year)
	players = nflgame.combine(games)

	if details == 'detailed':
		# this works to calculate games but specifying the team is MUCH faster:
		# #games = nflgame.games(year, home="PIT", away="PIT")
		#games = nflgame.games(year)
		bigben = nflgame.find(player)[0]
		# bigben -> Ben Roethlisberger (QB, PIT)
		# bigben.gsis_name -> B.Roethlisberger
		# bigben.position -> QB
		# bigben.team -> PIT

		# #TODO: complete this if logic for position-based stats
		# if bigben.position == 'QB':
		# 	# QB stats
		# if bigben.position == 'RB':
		# 	# RB stats
		# if bigben.position == 'WR':
		# 	# WR stats
		# if bigben.position == 'K':
		# 	# K stats
		
		# right now this is QB stats (hence the passing nomenclature)
		for i, game in enumerate(games):
		    if game.players.name(bigben.gsis_name):
		        stats = game.players.name(bigben.gsis_name).passing_yds
		        tds = game.players.name(bigben.gsis_name).passing_tds
		        response += '*Week {:2}* - {:3} yds, {:2} TD\n'.format(game.schedule['week'], stats, tds)

		response += '-'*25
		#players = nflgame.combine(games)
		response += '\n*{:4} Season - {:4} yds, {:2} TD*'.format(year, players.name(bigben.gsis_name).passing_yds, players.name(bigben.gsis_name).passing_tds)

	# if detailed stats are not requested, provide overall stats for the season
	else:
		#games = nflgame.games(year)
		#players = nflgame.combine(games)
		my_player = nflgame.find(player)[0]
		brady = players.name(my_player.gsis_name)
		response += '%d total yds, %d total TD in %d' % (brady.passing_yds, brady.passing_tds, year)

		# ne = nflgame.games(2010, home="NE", away="NE")
		# players = nflgame.combine(ne)
		# brady = players.name("T.Brady")
		# response += '%d, %d' % (brady.passing_tds, brady.passing_yds)

	message.reply(response)


#@respond_to('bio $', re.IGNORECASE)
@respond_to('bio (.*)', re.IGNORECASE)
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

@respond_to('game stats (.*) (.*) (.*)', re.IGNORECASE)
def get_game_stats(message, year, week, team):
	year = int(year)
	week = int(week)
	
	# nflgame requrires team abbreviations are uppercase
	game = nflgame.one(year,week=week,home=team.upper(),away=team.upper())
	
	# TODO: build actual validation for the year, week, team and improve the error reporting
	if len(year) <> 4:
		message.reply("NFL has been around for only the past 50ish years. Might want to try a 4 digit year")
		return
	if week > 25:
		message.reply("As much as I'd like, there aren't that many weeks in the NFL season")
		return
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