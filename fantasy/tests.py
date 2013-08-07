import fantasy as scraper
import unittest
import os

from BeautifulSoup import BeautifulSoup

# dir containing dummy html
DATA_DIR='test_data'

def file_abspath(fileName):
	'''
	Return absolute path of test data file

	returns: the path
	'''

	test_data_dir=os.path.split(os.path.abspath(__file__))[0]+os.sep+DATA_DIR
	return 'file://{0}/{1}'.format(test_data_dir,fileName)

class FantasyLoginTest(unittest.TestCase):

	def test_badLoginExcept(self):
		'''
		Bad login should raise an exception
		'''		
		try:
			l=scraper.FantasyLeague(scraper.USERNAME,'jpt',login=True)
		except Exception,e:
			self.assertEquals('Login failed ! Bad username/password ?', e.message,'Login test failed' )


class FantasyValuesTest(unittest.TestCase):

	def setUp(self):

		# the league class
		self.l=scraper.FantasyLeague(scraper.USERNAME,scraper.PASSWORD,login=False)

	def test_get_page(self):
		'''
		Get page should return a BeautifulSoup object
		'''

		page=self.l._get_page(file_abspath('my-leagues-page.html'))
		return self.assertIsInstance(page,BeautifulSoup)

	def test_league_links_parser(self):

		'''
		League links parser should return a dict 
		containing participated leagues
		'''

		result=self.l._parse_league_links(file_abspath('my-leagues-page.html'))

		# should be a dictionary and non-empty
		return self.assertIsInstance(result,dict) and self.assertTrue(len(result)!=0)

	def test_matchday_points_parser(self):
		'''
		Matchday points should be non-empty list
		'''
		points=self.l._parse_matchdayPoints(file_abspath('matchday-points.html'))

		return self.assertIsInstance(points,list) and self.assertTrue(len(points)!=0)

	def test_classic_league_parser(self):

		'''
		League table parser should return a non-empty dictionary
		'''
		table=self.l._parse_classic_league(file_abspath('private-classic-league.html'))

		return self.assertIsInstance(table,list) and assertIsTrue(len(table)!=0)

	def test_headtohead_league_parser(self):
		'''
		h2h table parser should return a non-empty dictionary
		'''
		table=self.l._parse_headtohead_league(file_abspath('private-headtohead-league.html'))

		return self.assertIsInstance(table,list) and assertIsTrue(len(table)!=0)

class FantasyBadInput(unittest.TestCase):

	def setUp(self):
		self.l=scraper.FantasyLeague(scraper.USERNAME,scraper.PASSWORD,login=False)

	def test_getLeague_except(self):
		''' 
		get_leagues() should throw an exception when 
		unsuported league type is passed as arg
		'''
		badValues=['chinaleague','japanleague','johndoe','lol']
		for v in badValues:			
			self.assertRaises(Exception,self.l.get_leagues,v)


if __name__=="__main__":
	unittest.main()