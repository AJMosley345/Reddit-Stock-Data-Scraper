from bs4 import BeautifulSoup
import requests

"""
Program that takes an HTML file and demonstrates various functions and methods of Beautiful Soup 4
"""

# Sends HTTP request that gets the HTML document
# Then creates a Beautiful Soup variable that has the HTML doc in it
# Finally prints the doc in a way that is more readable
url = "https://www.newegg.com/asus-geforce-rtx-3080-tuf-rtx3080-o10g-v2-gaming/p/N82E16814126525?Description=3080&cm_re=3080-_-14-126-525-_-Product&quicklink=true"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
# print(doc.prettify())

# Locating Text within a document
prices = doc.find_all(text="$") # Finds all text that is equal to "$"
parent = prices[0].parent # Gets the parent of the above statement
strong = parent.find("strong") # Finds the contents of the strong tag
print(strong.string)

def read_and_print():
    # Reads in an HTML file and parses it so Python can understand it
    with open("index.html", "r") as f:
        doc = BeautifulSoup(f, "html.parser")

    # Prints the HTML document
    print(doc.prettify())

    return doc

def find_by_tag():
    doc = read_and_print()
    # Find by tag name
    tag = doc.title
    tag.string = "hello" # Changes the string in the <title> tags to hello
    print("\n",tag) # Prints out everything string + tags
    print(tag.string, "\n") # Prints out just the string that is within the tags

    # Find all tags with that tag name
    tags = doc.find_all("a")
    print(tags, "\n") # Prints out all of the a tags in a list

    # Access nested tags
    tag2 = doc.find_all("p")[0]
    print(tag2.find_all("b"))