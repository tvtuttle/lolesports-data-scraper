# current function: scrapes match data from a gamepedia url and formats it into readable data
# goal function: scrapes match data, then formats data into fantasy excel spreadsheet for upload

import requests
from bs4 import BeautifulSoup
from contextlib import closing
import re

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
# player data will be stored in dictionary, with name as key
# when same playername appears, stats are added to existing entry
players = dict()
for div in html.find_all(class_='sb-p-info'):
    # get name
    name = div.contents[0].text
    # print(name)
    # get stats
    raw_stats = div.contents[1]
    # raw_stats contains kda, then cs, then gold; we just need kda and cs data
    raw_kda = raw_stats.contents[0].text
    cs = int(raw_stats.contents[1].text) # can just directly cast to int, might change this later

    # parse kda by getting numbers separated by slashes using regex
    kda = re.split('/', raw_kda)
    k = int(kda[0])
    d = int(kda[1])
    a = int(kda[2])

    # organize name and stats together into a list (not tuple, we need to change values), check and insert into dict
    if name not in players:
        players[name] = [k, d, a, cs]
    else:
        # add int values to existing name entry
        players[name][0] += k
        players[name][1] += d
        players[name][2] += a
        players[name][3] += cs

# Test: traverse dictionary and print names and related stats
for player in players:
    out = "{}: {}/{}/{}, {} cs"
    print(out.format(player, players[player][0], players[player][1], players[player][2], players[player][3]))

# organize teams and their relevant stats




