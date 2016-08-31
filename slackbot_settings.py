try:
	import config
except ImportError:
	print "config.py does not exist"

try:
	API_TOKEN = config.apitoken
except:
	print "API_TOKEN cannot be retrieved from config.py"

#DEFAULT_REPLY = "I support the following queries:\n"+"`top [position] [year]` - returns the top 5 players at a given position in a given year"

PLUGINS = [
	'mybot'
]

ERRORS_TO = 'lombardi_errors'
