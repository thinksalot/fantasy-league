import mechanize,cookielib,string
import login

# from output import *
from BeautifulSoup import BeautifulSoup

# main site url
SITE_MAIN='http://fantasy.premierleague.com'

# login page
SITE_LOGIN='https://users.premierleague.com/PremierUser/account/login.html'

# my-team url
MT_URL='http://fantasy.premierleague.com/my-team/'

# my-leagues url
ML_URL='http://fantasy.premierleague.com/my-leagues/'

# type of leagues
L_TYPES='classic headtohead global'.split()

class FantasyLeague(object):

    '''
    Implements a Fantasy Premiere League class
    '''

    def __init__(self,username,password,login=True):
        self.username=username
        self.password=password

        # current user's team name
        self.teamName=''

        # setup browser
        self.br=mechanize.Browser()
        self.br.set_handle_robots(False)

        # setup cookies
        cj=cookielib.LWPCookieJar()
        self.br.set_cookiejar(cj)

        if login:
            self._login()

    def _login(self):
        '''
        Authenticates user with given credentials

        raises: Exception when login was unsuccessful

        '''
        self.br.open(SITE_LOGIN)
        self.br.select_form(nr=0)
        self.br['j_username']=self.username
        self.br['j_password']=self.password
        self.br.method='POST'
        self.br.action=self.br.form.action

        response=BeautifulSoup(self.br.submit())

        # raises an exception if login fails
        if response.find('div',attrs={'id':'login-form-errors'})!=None:
            raise Exception('Login failed ! Bad username/password ?')

    def _get_page(self,url):

        '''
        Soupifies a html page

        url: a page url
        returns: a BeautifulSoup object

        raises: Exception when url couldnt be loaded
        '''
        # get event page
        try:
            r=self.br.open(url)        
            return BeautifulSoup(r.read())
        except:
            raise Exception('Cannot open url:'+url)

    def _get_matchdayLink(self,url):

        '''
        Returns the recent matchday url

        url: url of my-team page
        returns: the recent matchday url
        '''      
        page=self._get_page(url) 

        # get the horizontal navigation bar
        # and grab the recent matchday url         
        nav=page.find('nav')

        return SITE_MAIN+nav.findAll('li')[1].a['href']

    def _parse_league_links(self,page):

        '''
        Provided the my-leagues page, parses a list of participated leagues 

        page: url of my-leagues page
        returns: a dict containing all leagues

        '''
        page=self._get_page(page)    

        # get team name
        self.teamName=page.find('h2',attrs={'class':'ismMyLeague'}).string

        result={}
        for l in L_TYPES:
            result[l]=[]

        # league table classes
        #
        # we must provide all the classes a table belongs to
        # otherwise BeautifulSoup will return None
        #
        # for eg, passing {'classic':'ismPrivClassicLeague'} instead of
        # {'classic':'ismTable ismPrivClassicLeague'} wont work

        tableClasses={\
                    'classic':'ismTable ismPrivClassicLeague',\
                    'headtohead':'ismTable ismPrivH2HLeague',\
                    'global':'ismTable ismGlobalLeague'\
                    }

        for leagueType in tableClasses.keys():
            leagues=page.find(attrs={'class':tableClasses[leagueType]})

            # if not participating in any of the leagues
            if leagues is None:
                continue

            for league in leagues.findAll('tr'):
                columns=league.findAll('td')
                if len(columns)==0:
                    continue

                result[leagueType].append({\
                                'league':columns[0].a.string,\
                                'url':SITE_MAIN+columns[0].a['href'],\
                                'movement':string.strip(columns[1].img['alt']),\
                                'c_rank':string.strip(columns[2].string),\
                                'l_rank':string.strip(columns[3].string)
                            })
        return result

    def _parse_matchdayPoints(self,page):

        '''
        Parses a matchday's point

        page: a matchday event page
        returns: a list containing matchday points
        '''
        page=self._get_page(page)

        result=[]

        # find team players(without subs)        
        pitch=page.findAll(attrs={'class':'ismPitch'})[0]

        for player in pitch.findAll(attrs={'class':'ismElementDetail'}):
            # if some matches are yet to be played,
            # players have opposing team's name instead of points,
            # so assign 0
            try:
                point=int(player.dd.span.a.contents[1][3:])
            except:
                point=0
            pName=string.strip(player.dt.span.string)
            result.append({'player':pName,'point':point})            
        return result

    def _parse_classic_league(self,page):

        '''
        Parses a classic league table page

        page: url to a league ranking page
        returns: a list containing classic league ranks
        '''        
        page=self._get_page(page)

        result=[]

        # get leaderboard type
        title=page.find('h2',attrs={'class':'ismTabHeading'})
        result.append({'lbName':title.string,'lbType':'classic'})
        
        table=page.find('table')	        

        for row in table.findAll('tr'):

            data=row.findAll('td')

            # filter table headings
            if len(data)==0:
            	continue		
            rank=data[1].string
            team=data[2].a.string
            username=data[3].string	
            gwp=data[4].string
            tp=data[5].string   

            own=0
            if team==self.get_teamName():
                own=1         

            result.append({'rank':rank,'team':team,'user':username,'gwp':gwp,'total':tp,'self':own})

        return result

    def _parse_headtohead_league(self,page):

        '''
        Parses a headtohead league table page

        page: the url to headtohead league
        returns: a list containing headtohead league ranks
        '''
        page=self._get_page(page)

        result=[]

        # get leaderboard type
        title=page.find('h2',attrs={'class':'ismTabHeading'})
        result.append({'lbName':title.string,'lbType':'headtohead'})
        
        table=page.find(attrs={'class':'ismTable ismH2HStandingsTable'})
        

        for row in table.findAll('tr'):
            data=row.findAll('td')

            # filter table headings
            if len(data)==0:
                continue

            rank=data[1].string
            team=data[2].a.string
            wins=data[3].string
            draws=data[4].string
            losses=data[5].string
            totalPoints=data[6].string
            total=data[7].string

            result.append({'rank':rank,\
                            'team':team,\
                            'w':wins,\
                            'd':draws,\
                            'l':losses,\
                            '+':totalPoints,\
                            'pts':total
                })

        return result

    def _parse_global_league(self,league):

        '''
        Parses global league ranks

        return: a list of dictionaries 
        '''

        result=[]

        result.append({'lbType':'global','lbName':league['league']})
        result.append({\
            'lbType':'global',\
            'league':league['league'],\
            'c_rank':league['c_rank'],\
            'l_rank':league['l_rank'],\
            'movement':league['movement'],\
            'url':league['url']\
            })

        return result

    def get_teamName(self):
        '''
        Returns teamname of current user

        returns:a string indicating teamname
        '''
        return self.teamName


    def get_leagues(self,lType):

        '''
        Get user ranking on all leagues belonging
        to a particular type
        '''

        if lType not in L_TYPES:
            raise Exception('Unknown league type:%s'%lType)
        
        # get league urls
        leagues=self._parse_league_links(ML_URL)

        result=[]

        if lType in L_TYPES:
            for c in leagues[lType]:

                # 'dynamic' function name
                fName='_parse_'+lType+'_league'

                # global league parser take seperate set of data
                if lType=='global':
                    data_to_pass=c
                # all other leagues take league leaderboard url as param
                else:
                    data_to_pass=c['url']

                result.append(getattr(self,fName)(data_to_pass))

        return result

    def get_matchdayPoints(self):

        '''
        Get points scored in most recent matchday

        returns: an list of dict contaning player name and points
        '''

        # get recent mathchday page url
        matchday_url=self._get_matchdayLink(MT_URL)       

        return self._parse_matchdayPoints(matchday_url)
