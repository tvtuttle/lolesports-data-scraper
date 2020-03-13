# this file is for developing the format for input and output
# in both cases, there will be an excel spreadsheet with information regarding fantasy team and player choices
# after input, the spreadsheet will be filled with stats (from scraper), calculate fantasy points, and return a
# resulting sheet

# before setting up import, i'll need to decide what the spreadsheet will look like
# so, first, work on a demo fantasy spreadsheet on google sheets
# the input should just take the form of fantasy player, chosen team, chosen players
# similar to the status of last season's spreadsheets before stats were added, only without newly ignored stats
# (i.e. no first blood or elder dragon)

# todo: add case flexibility to player and team names (esp. player names)
# todo: add checks for validity of input file data and format


import pandas as pd
from gamepedia_fantasy_scraper import get_scoreboard
import numpy as np
from spreadsheet_formatting import output_fantasy_results
from player import FanTeam, LolPlayer, LolTeam


# some exceptions
class FantasyError(Exception):

    def __init__(self, message):
        # self.expression = expression
        self.message = message


# method to allow for more comprehensive checks when reading csv
def get_input(file):
    # first, determine the filename belongs to a csv
    try:
        data = pd.read_csv(file, header=0)
    except:
        raise FantasyError("Input CSV must be a .csv file")
    # todo: check formatting of user data
    return data


# put the main in a function with input from fantasy-lcs-main
def play_fantasy(input_filename, input_url, input_week, output_filename):
    # make sure input file is properly formatted
    # try:
    #     fantasy_data = pd.read_csv(input_filename, header=0)
    # except:
    #     print("Data is not stored in a csv format")
    fantasy_data = get_input(input_filename)
    # print(fantasy_data.columns.values)

    # get data from scraper
    try:
        [players, teams] = get_scoreboard(input_url)
    except:
        raise FantasyError("Error with scoreboard scraping; please make sure that input week/split is valid")
        # print("Error with scoreboard scraping -- you can't gather data from nonexistent games")

    # check fantasy_data player and team names against keys in players and teams
    print("Checking players...")
    for row in fantasy_data.iterrows():
        for entry in row[1]['Top':'Sub2']:
            if entry not in players:
                print(entry + " did not play, and thus has 0 points")
        # do same for teams
        if row[1]['Team'] not in teams:
            print(row[1]['Team'] + " is not a valid team name, and thus has 0 points")

    # now, do score calculations for each fantasy player
    # each player corresponds to a row
    # create dict of FanTeam objects that contain LolTeam, LolPlayers, etc.
    print("Calculating scores...")
    fantasy_results = dict()
    for row in fantasy_data.iterrows():
        row = row[1]  # reassignment for simplicity
        name = row['Name']
        color = row['Color']
        t = row['Team']
        fantasy_results[name] = FanTeam(name, color)
        for p in row['Top':'Sub2']:
            if p in players:
                fantasy_results[name].add_player(players[p])
            else:
                # get the row the player is in from team input (not scraper)
                # hackjob: just loop through all potential position columns and check presence
                pos = int()
                if p in row['Top']:
                    pos = 1
                elif p in row['Jungle']:
                    pos = 2
                elif p in row['Mid']:
                    pos = 3
                elif p in row['Bot']:
                    pos = 4
                elif p in row['Sup']:
                    pos = 0
                else:
                    pos = -1
                fantasy_results[name].add_player(LolPlayer(p, 0, 0, 0, 0, pos))
        # now for team stats
        if t in teams:
            fantasy_results[name].team = teams[t]
        # we'll include color as the final field
        else:
            # if t not in teams, all zeros
            fantasy_results[name].team = LolTeam(t, 0, 0, 0, 0, 0, 0)

    # swap bad starters with good subs using method in FanTeam
    for name in fantasy_results:
        fantasy_results[name].manage_roster()

    # we now have all the info required to determine winners
    # now the issue is formatting the output spreadsheet
    # trying to copy a hand-formatted style is difficult, but at the very least the output should be pleasing to read
    output_fantasy_results(output_filename, input_week, fantasy_results)







