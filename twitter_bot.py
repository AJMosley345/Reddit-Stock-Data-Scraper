import logging
import tweepy
import requests
from bs4 import BeautifulSoup
logger = logging.getLogger()

def get_weather(str):
    """Gets the weather of the parameter which is a string that contains the name of the city\n
       Prints out the temperature, the description of the sky and the day/time. 
    """
    # Get the weather for West Chester PA
    # Gets the html page for the weather and parses it so Python can understand it
    cityname = str
    url = "https://www.google.com/search?q="+"weather"+cityname
    weather_report = requests.get(url).content
    weather = BeautifulSoup(weather_report, 'html.parser')

    # Gets the temperature
    temp = weather.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

    # Gets the time and sky description
    str = weather.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    #Formats the data
    data = str.split(' ')

    # Gets the day
    day = data[0]

    # Formats the time
    time = data[1]
    am_pm = str[15:17]
    full_time = f"{time} {am_pm}"

    # Formats the sky description
    sky = str[18:50]

    weather_now = f"Today is {day}, it is {full_time}\nWeather in {cityname} is:\n{temp}\nIt is {sky}"

    return weather_now

def create_api():
    """Creates and authenticates the api that is created"""

    # Aethenticate to Twitter
    auth = tweepy.OAuthHandler("PxaluJaPBxBouSMTXPrGuG4Cm", 
    "nSJ2IMa2PDodN395SxL6kw7ejmdqjJNRtlQZVhCfojw1grvG4a")
    auth.set_access_token("1570658984-WO4TetVm6HOgNcZ2k2UEOZ0BZSVJ38Fe4mIntBa", 
    "okq3rA7wWrcczDE5PTBAzlr9jsV60KatN3G6WTI3GfCGE")

    # Makes an API object to get authentication
    bot = tweepy.API(auth, wait_on_rate_limit=True)

    # Authenticates the bot for use on Twitter
    try:
        bot.verify_credentials()
    except Exception as e:
        print("Error during authentication")
        logger.error("Error creating API", exc_info=True)

    logger.info("API created")
    return bot

weather_bot = create_api()
weather_bot.update_status(get_weather('West Chester'))