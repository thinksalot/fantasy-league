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

l=FantasyLeague(fantasy.USERNAME,fantasy.PASSWORD)
print_matchdayPoints(l.get_matchdayPoints())