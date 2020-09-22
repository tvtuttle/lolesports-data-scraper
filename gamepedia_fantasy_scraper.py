# current function: scrapes match data from a gamepedia url and formats it into readable data
# goal function: scrapes match data, then formats data into fantasy excel spreadsheet for upload
# TODO: all necessary functions implemented, now for ease-of-use io features

import requests
from bs4 import BeautifulSoup
from contextlib import closing
import re
from player import LolPlayer, LolTeam
import pandas as pd

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


# get scoreboard from wiki url
def get_scoreboard(url):
    raw_html = get_html(url)
    print("Checking for good response...")
    print(raw_html is not None)  # check for good response

    html = BeautifulSoup(raw_html, 'html.parser')

    # organize players and their relevant stats
    # player data will be stored in dictionary, with name as key
    # when same playername appears, stats are added to existing entry
    players = dict()
    pos = 0  # we'll use increments to determine player position via mod operator
    for div in html.find_all(class_='sb-p-info'):
        pos = pos + 1
        player_pos = pos % 5
        # KEY: 1 = top, 2 = jung, 3 = mid, 4 = bot, 0 = supp
        # get name
        name = div.contents[0].text
        # get stats
        raw_stats = div.contents[1]
        # raw_stats contains kda, then cs, then gold; we just need kda and cs data
        raw_kda = raw_stats.contents[0].text
        cs = int(raw_stats.contents[1].text)  # can just directly cast to int, might change this later

        # parse kda by getting numbers separated by slashes using regex
        kda = re.split('/', raw_kda)
        k = int(kda[0])
        d = int(kda[1])
        a = int(kda[2])

        # put name and stats into lolplayer object and store in dict keyed by name
        if name not in players:
            players[name] = LolPlayer(name, k, d, a, cs, player_pos)
        else:
            # add int values to existing name entry
            players[name].k += k
            players[name].d += d
            players[name].a += a
            players[name].cs += cs

    # organize teams and their relevant stats
    # there are three areas on the table from which to harvest team stats:
    # the top row (names), the sb-header (win/loss, gold, kills), and the sb-footer
    # we can also get the game time, from which we will generate the "fast win" stat
    # i.e. win < 30 mins = 1, else 0
    teams = dict()
    for div in html.find_all(class_='sb'):
        # we need to get 2 names per scoreboard
        # header entries are differentiated by side
        # looks like 2 footers per scoreboard?
        # so we'll collect two teams at once, put in organized 2-team list, then combine and add info to dict
        blue = list()
        red = list()
        names = div.find_all(class_='sb-teamname')
        blue_name = names[0].text
        red_name = names[1].text
        # september 2020 update: unicode characters were added around team names that broke this, so this should
        # remove the unicode characters
        blue_name = blue_name.encode("ascii", "ignore")
        blue_name = blue_name.decode()
        red_name = red_name.encode("ascii", "ignore")
        red_name = red_name.decode()
        blue_header = div.find(class_='side-blue')
        red_header = div.find(class_='side-red')
        blue_result = int(blue_header.text)
        red_result = int(red_header.text)
        footers = div.find_all(class_='sb-footer-stats')
        blue_footer = footers[0]
        red_footer = footers[1]
        # stats in footer are in order: towers, inhibs, barons, dragons, heralds
        # we will count everything except inhibs
        # with this, we will have all the stats we need (except first bloods, which we will ignore this season)
        # also, probably also not elder dragons; elder takes will count as much as regular dragon takes
        blue_towers = int(blue_footer.contents[0].text)
        blue_barons = int(blue_footer.contents[2].text)
        blue_dragons = int(blue_footer.contents[3].text)
        blue_heralds = int(blue_footer.contents[4].text)

        red_towers = int(red_footer.contents[0].text)
        red_barons = int(red_footer.contents[2].text)
        red_dragons = int(red_footer.contents[3].text)
        red_heralds = int(red_footer.contents[4].text)

        # now, check for sub 30 min win
        # no classes to cheat with so this will look ugly
        raw_time = div.contents[0].contents[2].contents[1].text
        time = re.split(':', raw_time)
        # guard against really long games (hour +)
        blue_fastwin = 0
        red_fastwin = 0
        if len(time) == 2:
            min = int(time[0])
            if (min < 30 and blue_result == 1):
                blue_fastwin = 1
            elif (min < 30 and red_result == 1):
                red_fastwin = 1

        # check for presence in team dict and then add accordingly
        if blue_name not in teams:
            teams[blue_name] = LolTeam(blue_name, blue_result, blue_towers, blue_barons, blue_dragons, blue_heralds, blue_fastwin)
        else:
            teams[blue_name].wins += blue_result
            teams[blue_name].towers += blue_towers
            teams[blue_name].barons += blue_barons
            teams[blue_name].dragons += blue_dragons
            teams[blue_name].heralds += blue_heralds
            teams[blue_name].fastwins += blue_fastwin

        # do the same for red
        if red_name not in teams:
            teams[red_name] = LolTeam(red_name, red_result, red_towers, red_barons, red_dragons, red_heralds, red_fastwin)
        else:
            teams[red_name].wins += red_result
            teams[red_name].towers += red_towers
            teams[red_name].barons += red_barons
            teams[red_name].dragons += red_dragons
            teams[red_name].heralds += red_heralds
            teams[red_name].fastwins += red_fastwin

    return [players, teams]


# a new scraping function, that creates a local database (well, actually a spreadsheet) of available players for a
# given league and season, with key identifying information
# this is the first step towards implementing player drafting and trades into the program
def get_players(url):
    raw_html = get_html(url)
    print("Checking for good response...")
    print(raw_html is not None)

    html = BeautifulSoup(raw_html, 'html.parser')
    # return html

    teams = html.find_all('span', class_="mw-headline")
    p_tables = html.find_all('table', class_= "wikitable hoverable-multirows sortable extended-rosters extended-rosters-hasres")
    # these should both have the same length, and each i in teams gives the team for the players at i in p_tables

    regions = list()
    positions = list()
    igns = list()
    irl_names = list()
    p_teams = list()
    for i in range(10):
        team = teams[i]
        p_table = p_tables[i]
        team_name = team.contents[0].contents[0].contents[0].get("title")
        print(team_name)  # bit messy, but it works
        # print(p_table)
        players = p_table.find_all('tr', class_='multirow-highlighter')
        for player in players:
            region = player.contents[0].text
            pos = player.contents[2].contents[0].get("title")
            ign = player.contents[3].text
            irl = player.contents[4].text
            print(region + ", " + pos + ", " + ign + ", " + irl)
            regions.append(region)
            positions.append(pos)
            igns.append(ign)
            irl_names.append(irl)
            p_teams.append(team_name)

    # now create series from lists
    regions = pd.Series(regions)
    positions = pd.Series(positions)
    igns = pd.Series(igns)
    irl_names = pd.Series(irl_names)
    p_teams = pd.Series(p_teams)

    # now create dict of series, and create dataframe from dict
    d = {'Region': regions,
         'Position': positions,
         'Ingame Name': igns,
         'Name': irl_names,
         'Team': p_teams}
    player_data = pd.DataFrame(d)
    # finally, export dataframe to a csv
    player_data.to_csv("player_data.csv")

if __name__ == "__main__":
    get_players("https://lol.gamepedia.com/LCS/2020_Season/Spring_Season/Team_Rosters")

    # # note: we are testing using the page for the now-complete spring 2020 lcs season
    # # as of this time (4/28/20), there is no team_roster page available for the upcoming season
    # # thus, this program will not be able to get information from the summer 2020 season until it is updated
    # html = get_players("https://lol.gamepedia.com/LCS/2020_Season/Spring_Season/Team_Rosters")
    # # each tr element is a table row, and the player and coach rows have this class (other classes for different data)
    # divs = html.find_all('tr', class_='multirow-highlighter')
    # # under each tr element, we find:
    # # 0: region eligibility -- can be extracted
    # print(divs[0].contents[0])
    # # 1: country flag image -- cannot be extracted
    # # home country has no effect on player eligibility, only region, so we can ignore this
    # print(divs[0].contents[1])
    # # 2: role -- can be extracted
    # print(divs[0].contents[2])
    # # 3: player in game name -- can be extracted
    # print(divs[0].contents[3])
    # # 4: player real name -- can be extracted
    # print(divs[0].contents[4])
    # # all further contents involve games played in a season -- not relevant
    # # if we want to find the team the player is playing for, we will have to search for a tag above this one
    # # specifically, the team name for the players is located in a section before their respective table
    # # each is marked as an html h3
    # team_divs = html.find_all('h3')
    # print(team_divs[0])
    # # after this, we look at the next table with the correct tags, then extract player data from each of its rows
    # tables = html.find_all('table', class_= "wikitable hoverable-multirows sortable extended-rosters extended-rosters-hasres")
    # print(tables[0].text)
    # # therefore, in the page, we can get the team by looking at each table with the above class, and players on each team
    # # by looking at the tr objects with appropriate class within


