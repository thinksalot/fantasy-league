import os
import sys

# imports the fantasy module
try:
	import fantasyleague
except:
	modulePath=os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
	sys.path.append(modulePath)
	from fantasy import *	

from output import *

l=FantasyLeague(login.USERNAME,login.PASSWORD)

# print all league leaderboards
for league in fantasy.L_TYPES:
	for ranks in l.get_leagues(league):
		print_leaderboard(ranks)
