# this file is for developing the format for input and output
# in both cases, there will be an excel spreadsheet with information regarding fantasy team and player choices
# after input, the spreadsheet will be filled with stats (from scraper), calculate fantasy points, and return a
# resulting sheet

# before setting up import, i'll need to decide what the spreadsheet will look like
# so, first, work on a demo fantasy spreadsheet on google sheets
# the input should just take the form of fantasy player, chosen team, chosen players
# similar to the status of last season's spreadsheets before stats were added, only without newly ignored stats
# (i.e. no first blood or elder dragon)

import pandas as pd
from gamepedia_fantasy_scraper import get_scoreboard
import numpy as np

# import simple input spreadsheet using pandas and read as dataframe
fantasy_data = pd.read_csv("lcs fantasy test - mock input.csv", header=0)
print(fantasy_data.columns.values)

# get data from scraper
[players, teams] = get_scoreboard('https://lol.gamepedia.com/LCS/2019_Season/Summer_Season/Scoreboards/Week 2')

# review scraper output
print("Test: Player stats for Week 2, Summer 2019")
for player in players:
    out = "In Position {}, {}: {}/{}/{}, {} cs"
    print(out.format(players[player][4], player, players[player][0], players[player][1], players[player][2], players[player][3]))

print("Test: Team stats for Week 2, Summer 2019")
for team in teams:
    out = "{}: {} wins, {} towers, {} barons, {} dragons, {} rift heralds, {} <30 min wins"
    print(out.format(team, teams[team][0], teams[team][1], teams[team][2], teams[team][3], teams[team][4], teams[team][5]))

# check fantasy_data player names against keys in players, then process scores
tops = fantasy_data.loc[:,'Sub2']
tops = tops.astype('str')
for top in tops:
    print(top)
    print(top in players)



