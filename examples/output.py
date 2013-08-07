from prettytable import PrettyTable

def print_header(title=''):
    print 
    print '*'*50    
    print '{0:}'.format(title)
    print '*'*50
    print 

def print_matchdayPoints(mpList):

    # print a stylish header
    print_header('Mathchday points')

    t=PrettyTable(['Player','Points'])    
    t.align['Player']='l'
    t._set_padding_width(1)

    total=0
    for player in mpList:
        total+=player['point']
        t.add_row([player['player'],player['point']])        

    t.add_row(['-'*10,'-'*5])
    t.add_row(['Total',total])

    print t

def print_leaderboard(league): 

    if league[0]['lbType']=='classic':
        _print_classic_league_rank(league[1:])
    elif league[0]['lbType']=='headtohead':        
        _print_h2h_league_rank(league[1:])
    elif league[0]['lbType']=='global':
        _print_global_league_rank(league[1:])

def _print_classic_league_rank(lTable):
    print_header('Classic League')    

    # print title
    t=PrettyTable('Rank Team Player GWP Total'.split())   
    t.align['Team']='l' 
    t.align['Player']='l' 

    for item in lTable:        
        t.add_row([item['rank'],item['team'],item['user'],item['gwp'],item['total']])

    print t        

def _print_h2h_league_rank(lTable):
    print_header('Headtohead League')

    t=PrettyTable('Rank Team W D L + Pts'.split())
    t.align['Team']='l'

    for item in lTable:
        t.add_row([item[key] for key in 'rank team w d l + pts'.split()])
        # print item  
    print t      

def _print_global_league_rank(lTable):

    print_header('Global League')

    # print title
    t=PrettyTable('League Movement Current-Rank Last-Rank'.split())    
    t.align['League']='l'

    for item in lTable:
        # print item
        t.add_row([item[key] for key in 'league movement c_rank l_rank'.split()])
        
    print t
