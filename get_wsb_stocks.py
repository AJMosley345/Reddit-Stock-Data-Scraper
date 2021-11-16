#region imports and global variables
import pandas as pd
import praw
from bs4 import BeautifulSoup
from yahoo_fin import stock_info as si
from slowprint.slowprint import slowprint
# Creation of reddit instance
reddit = praw.Reddit(
    client_id='2a5_2RZA_qNrdMZw9c5uEg', 
    client_secret='ypCn3ljSq64KBtVuIKPjr9qShyEeNg',
    user_agent='Stock Data Scraping'
)
#endregion

def getID():
    subreddit = reddit.subreddit('wallstreetbets').hot()
    for sub in subreddit:
        if sub.link_flair_text == "Daily Discussion":
            id = sub
            break
    return id

wsb_dd_id = getID()
wsb_m_id = 'qtzc0g'


#region getting and parsing content
def getDiscussionComments(wsb_dd_id):
    """
    Gets the comments from the r/WallStreetBets and returns it as html text
    """
    wsb_html_file = ""
    # Gets the daily discussion post
    wsb_post = reddit.submission(id = wsb_dd_id)

    # Removes the MoreComments error
    wsb_post.comments.replace_more(limit=0)

    # Gets the comments of the wsb post and stores them in the wsb_html_file
    for comments in wsb_post.comments.list():
        wsb_html_file += comments.body_html

    return wsb_html_file

def parseWSBHTML(wsb_html):
    #region variables
    wsb_comment_list = []
    p_list = []
    wsb_com = BeautifulSoup(wsb_html, "lxml")
    wsb_div_container = wsb_com.find_all("div", class_="md")
    #endregion

    #region print and append
    for i in wsb_div_container:
        p_list.append(i.find('p'))
        for j in p_list:
            wsb_comment_list.append(str(j))
    #endregion
    return wsb_comment_list
#endregion

#region getting lists
def getMostActiveSymbols():
    """Returns a list of the most active symbols from yahoo_fin"""
    symbol_list = []
    most_active = si.get_day_most_active(count=100)

    for i in most_active.index:
        symbols = most_active['Symbol'][i]
        symbol_list.append(symbols)

    return symbol_list

def wsbList(wsb_list):
    pop_list = []
    [pop_list.append(i) for i in wsb_list]
    return pop_list

def getAndParseSub():
    #region getting and parsing html content
    wsb_file = getDiscussionComments(wsb_dd_id)
    wsb_list = parseWSBHTML(wsb_file)
    pop_list = wsbList(wsb_list)
    #endregion

    return pop_list
#endregion

def getPopularWSBTickers():
    #region function calls and variables
    wsb_dataset, split_list, full_list, df = [], [], [], {}
    i = 0
    wsb_list = getAndParseSub()
    symbol_list = getMostActiveSymbols()
    #endregion

    # Splits the comments of wsb into a list, then each element is appended to the full list
    [split_list.append(i.split(" ")) for i in wsb_list]
    for j in split_list:
        [full_list.append(l) for l in j]

    # Finds matches for uppercase, lowercase and tickers with dollar signs
    for words in full_list:
        for symbols in symbol_list:
            if words == symbols:
                wsb_dataset.append(symbols)
            elif words == symbols.lower():
                wsb_dataset.append(symbols.lower())
    
    # Finds how many times a ticker occurs in the data set
    for tickers in wsb_dataset:
        lit_list = [{
            'ticker': tickers,
            'occurs': str(wsb_dataset.count(tickers)), 
            'lowercase': str(wsb_dataset.count(tickers.lower()))
        }]
        for stuff in lit_list:
            df[i] = {
                "Ticker": stuff['ticker'], 
                "Occurs": stuff['occurs'],
                "Lowercase": stuff['lowercase']
            }
            i += 1

    wsb_dataframe = pd.DataFrame.from_dict(df, "index").drop_duplicates().reset_index().sort_values(['Ticker'])
    return wsb_dataframe

def popTickersList():
    wsb_dataset = getPopularWSBTickers()
    pop_list = wsb_dataset.Ticker.tolist()
    return pop_list

def occurs():
    wsb_occurs = getPopularWSBTickers()
    full_list = []
    pop_list = wsb_occurs.Ticker.tolist()
    occurs_list = wsb_occurs.Occurs.tolist()
    full_list.append(pop_list)
    full_list.append(occurs_list)
    return full_list

def runWSB():
    pop_list = occurs()
    i = 0

    occur = pop_list[1]
    occur = [int(i) for i in occur]
    # tickers = pop_list[0]

    # for ticker in tickers:

    slowprint("Most talked about stocks on r/WallStreetBets", .3)
    while i < len(pop_list[0]):
        if pop_list[0][i] == pop_list[0][i].lower():
            pop_list[0].remove(pop_list[0][i].lower())
            occur[i] += occur[i]
            i += 1
        else:
            slowprint(pop_list[0][i], .3)
            print(occur[i], "\n")
            i += 1
