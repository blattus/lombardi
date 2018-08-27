import os

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    espn_s2 = os.environ.get('ESPN_S2',None)
    swid = os.environ.get('SWID',None)
    league_id = os.environ.get('LEAGUE_ID',None)
    year = os.environ.get('YEAR',None)
    stattleship_token = os.environ.get('STATTLESHIP_TOKEN',None)

    # umm should probably do this with proper environment vars but let's see if this works?
    f = open('config.py','w+')
    f.write('espn_s2 = \'{}\'\n'.format(espn_s2))
    f.write('swid = \'{}\'\n'.format(swid))
    f.write('league_id = {}\n'.format(league_id))
    f.write('year = {}\n'.format(year))
    f.write('stattleship_token = \'{}\'\n'.format(stattleship_token))
    f.close()

try:
	import config
except ImportError:
	print("config.py does not exist")

try:
	API_TOKEN = config.apitoken
except:
	print("API_TOKEN cannot be retrieved from config.py")


DEFAULT_REPLY = "Hmm, not sure I can do with that. Try `help`"

PLUGINS = [
	'mybot',
	'espn',
	'nflstats',
    'sleeper'
]

ERRORS_TO = 'lombardi_errors'
