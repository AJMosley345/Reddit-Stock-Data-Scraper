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
s_id = 'qv4wv4'
#endregion

#region getting and parsing content
def getStocksComments(s_id):
    s_html_file = ""
    s_post = reddit.submission(id = s_id)

    s_post.comments.replace_more(limit=0)

    for comments in s_post.comments.list():
        s_html_file += comments.body_html

    return s_html_file

def parseStockHTML(s_html):
    s_comment_list = []
    stock_com = BeautifulSoup(s_html, "lxml")
    stock_div_container = stock_com.find_all("div", class_="md")
    for i in stock_div_container:
        s_text = i.p.text
        s_comment_list.append(s_text)
    return s_comment_list

def stocksList(s_comment_list):
    pop_list = []
    [pop_list.append(i) for i in s_comment_list]
    return pop_list

def getAndParseSub():
    #region getting and parsing html content
    stock_file = getStocksComments(s_id)
    stocks_list = parseStockHTML(stock_file)
    pop_list = stocksList(stocks_list)
    #endregion

    return pop_list
#endregion

#region getting and comparing tickers
def getMostActiveSymbols():
    """Returns a list of the most active symbols from yahoo_fin"""
    symbol_list = []
    most_active = si.get_day_most_active(count=100)

    for i in most_active.index:
        symbols = most_active['Symbol'][i]
        symbol_list.append(symbols)

    return symbol_list

def getPopularStocksTickers():
    #region function calls and variables
    stocks_dataset, split_list, full_list, df = [], [], [], {}
    i = 0
    stocks_list = getAndParseSub()
    symbol_list = getMostActiveSymbols()
    #endregion

    # Splits the comments of wsb into a list, then each element is appended to the full list
    [split_list.append(i.split(" ")) for i in stocks_list]
    for j in split_list:
        [full_list.append(l) for l in j]

    # Finds matches for uppercase, lowercase and tickers with dollar signs
    for words in full_list:
        for symbols in symbol_list:
            if words == symbols:
                stocks_dataset.append(symbols)
            elif words == symbols.lower():
                stocks_dataset.append(symbols.lower())
            # elif words == ("$" + symbols):
            #     stocks_dataset.append(symbols)
    
    # Finds how many times a ticker occurs in the data set
    for tickers in stocks_dataset:
        lit_list = [{
            'ticker': tickers,
            'occurs': str(stocks_dataset.count(tickers)), 
            'lowercase': str(stocks_dataset.count(tickers.lower()))
        }]
        for stuff in lit_list:
            df[i] = {
                "Ticker": stuff['ticker'], 
                "Occurs": stuff['occurs'],
                "Lowercase": stuff['lowercase']
            }
            i += 1


    stocks_dataframe = pd.DataFrame.from_dict(df, "index")
    return stocks_dataframe
#endregion

def popTickersListStock():
    wsb_dataset = getPopularStocksTickers()
    pop_list = wsb_dataset.Ticker.tolist()
    return pop_list

def runStocks():
    pop_list = popTickersListStock()
    slowprint("Current Price of the most talked about stocks on r/Stocks\n", .3)
    for tickers in pop_list:
        f_prince = "%.2f" % si.get_live_price(tickers)
        f_string = f'{tickers}:\n{f_prince}'
        slowprint(f_string, .3)

