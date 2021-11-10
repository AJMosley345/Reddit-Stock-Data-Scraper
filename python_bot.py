import praw

# Creation of reddit instance
reddit = praw.Reddit(
    client_id='2a5_2RZA_qNrdMZw9c5uEg', 
    client_secret='ypCn3ljSq64KBtVuIKPjr9qShyEeNg',
    user_agent='Stock Data Scraping'
)

def openAndWriteFile(wsb_file, s_file):
    """
    Takes the text made by getDiscussionComments() and writes it to an html file
    """
    with open('wsb_comments.html', 'w') as f:
        f.truncate()
        f.write(wsb_file)
    with open('s_comments.html', 'w') as f:
        f.truncate()
        f.write(s_file)

def getDiscussionComments(wsb_id, s_id):
    """
    Gets the comments from the r/WallStreetBets & r/Stocks and returns it as html text
    """
    wsb_html_file = ""
    s_html_file = ""
    # Gets the daily discussion post
    wsb_post = reddit.submission(id = wsb_id)
    s_post = reddit.submission(id = s_id)

    # Removes the MoreComments error
    wsb_post.comments.replace_more(limit=0)
    s_post.comments.replace_more(limit=0)

    # Gets the comments of the wsb post and stores them in the wsb_html_file
    for comments in wsb_post.comments.list():
        wsb_html_file += comments.body_html
        # print(comments.body_html)
    
    for comments in s_post.comments.list():
        s_html_file += comments.body_html

    return wsb_html_file, s_html_file

wsb_id = 'qqrw8d'
s_id = 'qqrg59'

wsb_file, s_file = getDiscussionComments(wsb_id, s_id)

openAndWriteFile(wsb_file, s_file)