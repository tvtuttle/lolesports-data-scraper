# this file is for developing the format for input and output
# in both cases, there will be an excel spreadsheet with information regarding fantasy team and player choices
# after input, the spreadsheet will be filled with stats (from scraper), calculate fantasy points, and return a
# resulting sheet

# before setting up import, i'll need to decide what the spreadsheet will look like
# so, first, work on a demo fantasy spreadsheet on google sheets
# the input should just take the form of fantasy player, chosen team, chosen players
# similar to the status of last season's spreadsheets before stats were added, only without newly ignored stats
# (i.e. no first blood or elder dragon)

# stretch goals (to do later):
#   add case flexibility to player and team names

import pandas as pd
from gamepedia_fantasy_scraper import get_scoreboard
import numpy as np
from spreadsheet_formatting import output_fantasy_results

# import simple input spreadsheet using pandas and read as dataframe
if __name__ == '__main__':
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

    # check fantasy_data player and team names against keys in players and teams
    print("Checking players...")
    for row in fantasy_data.iterrows():
        for entry in row[1]['Top':'Sub2']:
            if entry not in players:
                print(entry + " did not play, and thus is ignored")
        # do same for teams
        if row[1]['Team'] not in teams:
            print(row[1]['Team'] + " is not a valid team name, and thus is ignored")

    # now, do score calculations for each fantasy player
    # incidentally, each player corresponds to a row
    # we will store calculations once again in a dict of stat lists, keyed by fantasy player name
    print("Calculating scores...")
    fantasy_results = dict()
    for row in fantasy_data.iterrows():
        row = row[1] # reassignment for simplicity
        name = row['Name']
        color = row['Color']
        t = row['Team']
        total_score = 0
        print(name)
        fantasy_results[name] = list()
        for p in row['Top':'Sub2']:
            if p in players:
                p_stats = players[p]
                # print(p_stats)
                # scores are calculated as follows:
                # 2*kills + 1.5*assists + 0.01*cs - 0.5*deaths
                score = round(2*p_stats[0] - 0.5*p_stats[1] + 1.5 * p_stats[2] + 0.01*p_stats[3], 2)
                # print(score)
                fantasy_results[name].append((p, score, p_stats[4]))
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
                fantasy_results[name].append((p, 0, pos))
        # now for team stats
        if t in teams:
            t_stats = teams[t]
            print(t_stats)
            # team scores are calculated as follows:
            # 2*wins + 1*towers + 2*barons + 1*dragons + 2*heralds + 2* sub 30 win
            score = round(2*t_stats[0] + t_stats[1] + 2*t_stats[2] + t_stats[3] + 2*t_stats[4] + 2*t_stats[5], 2)
            fantasy_results[name].append((t, score))
        # we'll include color as the final field
        fantasy_results[name].append(color)

    for name in fantasy_results:
        print(name + ": " + str(fantasy_results[name]))


    # now that dict of fantasy players is filled, we determine final scores of each player
    final_results = dict()
    for f in fantasy_results:
        # final score is determined by taking all player entries (tuples of length 3)
        # and summing the highest score of player entries with unique positions
        final_roster = dict()
        final_subs = dict()
        final_score = 0
        # everything below here is being changed to accommodate spreadsheet needs
        for p in fantasy_results[f]:
            if type(p) is tuple and len(p) == 3:
                if p[0] not in players:
                    players[p[0]] = [0, 0, 0, 0, p[2]] # doing this now because position calculation was earlier
                    # may want to later change for ease of understanding
                if p[2] not in final_roster and p[2] > -1:
                    final_roster[p[2]] = (p[0], p[1])
                elif p[2] in final_roster and p[1] > final_roster[p[2]][1]:
                    final_subs[p[2]] = final_roster[p[2]]
                    final_roster[p[2]] = (p[0], p[1])
                else:
                    final_subs[p[2]] = (p[0], p[1])
        # print(final_roster)
        # final results format: dict of starters, dict of subs (both keyed by position num), team tuple, color, total score
        # calculating total score now: starters points + team points
        for p in final_roster:
            final_score += final_roster[p][1]
        final_score += fantasy_results[f][-2][1]
        final_score = round(final_score, 2)
        final_results[f] =(final_roster, final_subs, fantasy_results[f][-2], fantasy_results[f][-1], final_score)
        # now the last entry in each player entry for fantasy results dict is
        # another dict representing the final displayed roster

    # now our fantasy_results dict is loaded with the information we need to make an output spreadsheet
    # just got to remember to access the information correctly
    # to review, let's print
    print("Output after calculations:")
    for f in final_results:
        print(f)
        print(final_results[f])
    # for f in fantasy_results:
    #     print(f)
    #     print(fantasy_results[f])

    # we now have all the info required to determine winners
    # now the issue is formatting the output spreadsheet
    # trying to copy a hand-formatted style is difficult, but at the very least the output should be pleasing to read
    output_fantasy_results(final_results, players, teams)







