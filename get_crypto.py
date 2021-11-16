#region imports and global variables
import pandas as pd
import praw
from bs4 import BeautifulSoup
import cbpro
from slowprint.slowprint import slowprint
# Creation of reddit instance
reddit = praw.Reddit(
    client_id='2a5_2RZA_qNrdMZw9c5uEg', 
    client_secret='ypCn3ljSq64KBtVuIKPjr9qShyEeNg',
    user_agent='Stock Data Scraping'
)
pc = cbpro.PublicClient()
crypto_dd_id = 'quu6t2'
#endregion


#region getting and parsing content
def getDiscussionComments(crypto_dd_id):
    """
    Gets the comments from the r/WallStreetBets and returns it as html text
    """
    crypto_html_file = ""
    # Gets the daily discussion post
    crypto_post = reddit.submission(id = crypto_dd_id)

    # Removes the MoreComments error
    crypto_post.comments.replace_more(limit=0)

    # Gets the comments of the crypto post and stores them in the crypto_html_file
    for comments in crypto_post.comments.list():
        crypto_html_file += comments.body_html

    return crypto_html_file

def parsecryptoHTML(crypto_html):
    #region variables
    crypto_comment_list = []
    p_list = []
    crypto_com = BeautifulSoup(crypto_html, "lxml")
    crypto_div_container = crypto_com.find_all("div", class_="md")
    #endregion

    #region print and append
    for i in crypto_div_container:
        p_list.append(i.find('p'))
        for j in p_list:
            crypto_comment_list.append(str(j))
    #endregion
    return crypto_comment_list
#endregion

#region getting lists
def getTopCrypto():
    """Returns a list of the most active crypto symbols"""
    crypto_list = ['BTC', 'ETH', 'USDT', 'ADA', 'DOGE', 'AVAX', 'SHIB', 'DOT', 'LTC', 'SOL']
    return crypto_list

def cryptoList(crypto_list):
    pop_list = []
    [pop_list.append(i) for i in crypto_list]
    return pop_list

def getAndParseSub():
    #region getting and parsing html content
    crypto_file = getDiscussionComments(crypto_dd_id)
    crypto_list = parsecryptoHTML(crypto_file)
    pop_list = cryptoList(crypto_list)
    #endregion

    return pop_list
#endregion

def getPopularCryptoTickers():
    #region function calls and variables
    crypto_dataset, split_list, full_list, df = [], [], [], {}
    i = 0
    crypto_list = getAndParseSub()
    symbol_list = getTopCrypto()
    #endregion

    # Splits the comments of crypto into a list, then each element is appended to the full list
    [split_list.append(i.split(" ")) for i in crypto_list]
    for j in split_list:
        [full_list.append(l) for l in j]

    # Finds matches for uppercase, lowercase and tickers with dollar signs
    for words in full_list:
        for symbols in symbol_list:
            if words == symbols:
                crypto_dataset.append(symbols)
            elif words == symbols.lower():
                crypto_dataset.append(symbols.lower())
    
    # Finds how many times a ticker occurs in the data set
    for tickers in crypto_dataset:
        lit_list = [{
            'ticker': tickers,
            'occurs': str(crypto_dataset.count(tickers)), 
            'lowercase': str(crypto_dataset.count(tickers.lower()))
        }]
        for stuff in lit_list:
            df[i] = {
                "Ticker": stuff['ticker'], 
                "Occurs": stuff['occurs'],
                "Lowercase": stuff['lowercase']
            }
            i += 1

    crypto_dataframe = pd.DataFrame.from_dict(df, "index").drop_duplicates().reset_index().sort_values(['Ticker'])
    return crypto_dataframe

def popTickersList():
    crypto_dataset = getPopularCryptoTickers()
    pop_list = crypto_dataset.Ticker.tolist()
    return pop_list

def runCrypto():
    #crypto_dataframe = getPopularTickers()
    pop_list = popTickersList()
    i = 0
    while i < len(pop_list):
        for j in pop_list:
            pop_list[i] = (j.upper() + '-USD')
            i += 1
    slowprint("Prices of the most talked about crypto on r/Cryptocurrency\n", .2)
    for items in set(pop_list):
        crypto = pc.get_product_ticker(product_id= items)
        price = crypto['price']
        f_string = f'{items}:\n{price}\n'
        slowprint(f_string, .2)
