import webbrowser
import re
from urllib.parse import urlparse
import praw
# webbrowser.open("https://www.reddit.com/r/wallstreetbets/", new=2)
reddit = praw.Reddit(
    client_id='2a5_2RZA_qNrdMZw9c5uEg', 
    client_secret='ypCn3ljSq64KBtVuIKPjr9qShyEeNg',
    user_agent='Stock Data Scraping'
)

subreddit = reddit.subreddit('wallstreetbets')
for item in subreddit.gilded():
    print(item)

# reddit.submission()