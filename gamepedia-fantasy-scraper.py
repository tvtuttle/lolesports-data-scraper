# current function: scrapes match data from a gamepedia url and formats it into readable data
# goal function: scrapes match data, then formats data into fantasy excel spreadsheet for upload

import requests
from bs4 import BeautifulSoup
from contextlib import closing

# create function to download webpage data from internet
# based on tutorial code from https://realpython.com/python-web-scraping-practical-introduction/


def get_html(url):
    # use try except structure to account for html code errors
    try:
        with closing(requests.get(url, stream=True)) as resp: # closing frees network resources when with is out of scope
            if good_response(resp):
                return resp.content
            else:
                return None

    except requests.RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e))) # with format, url is 0, exception 1


def good_response(resp):

    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


# for now, url will be a fixed value here: will add user input later
# currently using old statistics from 2019 summer, hopefully wiki format does not change, will update if so
url = 'https://lol.gamepedia.com/LCS/2019_Season/Summer_Season/Scoreboards' # week 1 stats, later weeks append(/Week_#)

raw_html = get_html(url)
print(raw_html is not None) # check for good response

html = BeautifulSoup(raw_html, 'html.parser')

# organize players and their relevant stats
for div in html.find_all(class_='sb-p-info'):




# organize teams and their relevant stats




