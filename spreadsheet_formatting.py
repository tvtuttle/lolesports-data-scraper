# this file contains functions involving the openpyxl package
# isolated from other code files because this could get messy

import openpyxl

def output_fantasy_results(results, players, teams):
    # currently assuming results take format of final_results from fantasy_spreadsheet_io (i.e. a dict of tuples with
    # 2 dicts: starting players and relevant scores, and sub players with relevant scores
    # if we want to fill the sheet with all the stats used to find scores, we can expand that functionality later
    # additionally assuming players and teams take the form of scraped player and team data
    wb = openpyxl.Workbook()
    dest_filename = 'fantasy_book.xlsx'

    ws1 = wb.active
    ws1.title = "Test 2019 Week 2 Results"

    # the rows written to are relative to the number of players in the game
    # we can get these from looping through results
    row = 2
    for name in results:
        print(name)
        ws1['A'+str(row)] = name
        # space after name
        row += 2
        # fill in column headers for team stats
        ws1['C'+str(row)] = "Wins"
        ws1['D'+str(row)] = "Towers"
        ws1['E'+str(row)] = "Barons"
        ws1['F' + str(row)] = "Dragons"
        ws1['G' + str(row)] = "Rift Heralds"
        ws1['H' + str(row)] = "<30 Min Wins"
        ws1['J' + str(row)] = "Team Points"
        row += 1
        ws1['A' + str(row)] = "Team"
        team = results[name][2][0]
        ws1['B' + str(row)] = team
        # now, fill in team stats from teams and final score from results
        ws1['C'+str(row)] = teams[team][0]
        ws1['D' + str(row)] = teams[team][1]
        ws1['E' + str(row)] = teams[team][2]
        ws1['F' + str(row)] = teams[team][3]
        ws1['G' + str(row)] = teams[team][4]
        ws1['H' + str(row)] = teams[team][5]
        ws1['J' + str(row)] = results[name][2][1]
        row += 1
        # player stat headers
        ws1['C' + str(row)] = "Kills"
        ws1['D' + str(row)] = "Deaths"
        ws1['E' + str(row)] = "Assists"
        ws1['F' + str(row)] = "CS"
        ws1['G' + str(row)] = "Totals"
        row += 1
        # player entries for each position
        # individual stats from players, name and score from results
        ws1['A' + str(row)] = "Top"
        top = results[name][0][1][0]
        ws1['B' + str(row)] = top
        ws1['C' + str(row)] = players[top][0]
        ws1['D' + str(row)] = players[top][1]
        ws1['E' + str(row)] = players[top][2]
        ws1['F' + str(row)] = players[top][3]
        ws1['G' + str(row)] = results[name][0][1][1]
        row += 1

        ws1['A' + str(row)] = "Jungle"
        jung = results[name][0][2][0]
        ws1['B' + str(row)] = jung
        ws1['C' + str(row)] = players[jung][0]
        ws1['D' + str(row)] = players[jung][1]
        ws1['E' + str(row)] = players[jung][2]
        ws1['F' + str(row)] = players[jung][3]
        ws1['G' + str(row)] = results[name][0][2][1]
        row += 1

        ws1['A' + str(row)] = "Mid"
        mid = results[name][0][3][0]
        ws1['B' + str(row)] = mid
        ws1['C' + str(row)] = players[mid][0]
        ws1['D' + str(row)] = players[mid][1]
        ws1['E' + str(row)] = players[mid][2]
        ws1['F' + str(row)] = players[mid][3]
        ws1['G' + str(row)] = results[name][0][3][1]
        row += 1

        ws1['A' + str(row)] = "Bot"
        bot = results[name][0][4][0]
        ws1['B' + str(row)] = bot
        ws1['C' + str(row)] = players[bot][0]
        ws1['D' + str(row)] = players[bot][1]
        ws1['E' + str(row)] = players[bot][2]
        ws1['F' + str(row)] = players[bot][3]
        ws1['G' + str(row)] = results[name][0][4][1]
        row += 1

        ws1['A' + str(row)] = "Support"
        supp = results[name][0][0][0]
        ws1['B' + str(row)] = supp
        ws1['C' + str(row)] = players[supp][0]
        ws1['D' + str(row)] = players[supp][1]
        ws1['E' + str(row)] = players[supp][2]
        ws1['F' + str(row)] = players[supp][3]
        ws1['G' + str(row)] = results[name][0][0][1]
        row += 2

        # because sub dict uses weird entries, i think i need to loop through
        # should be inexpensive, just 2 per
        # TODO: finish this, and figure out how to deal with players without stats (if/else?)
        # sub_num = 1
        # for sub in results[name][1]:
        #     sub_name = sub[0]
        #     ws1['A' + str(row)] = "Sub-"+str(sub_num)
        #     ws1['B' + str(row)] = sub_name
        #     ws1['C' + str(row)] = players[sub_name][0]
        #     ws1['D' + str(row)] = players[sub_name][1]
        #     ws1['E' + str(row)] = players[mid][2]
        #     ws1['F' + str(row)] = players[mid][3]
        #     ws1['G' + str(row)] = results[name][0][3][1]
        #     row += 1

    wb.save(dest_filename)

if __name__ == "__main__":
    output_fantasy_results("foobar", "o", "o")