# this file contains functions involving the openpyxl package
# isolated from other code files because this could get messy

import openpyxl

def name_colors():
    # outputs a dict of colors, all hex codes keyed by name
    # for now, just the one's used last year
    color = dict()
    color["Red"] = "FF0000"
    color["Green"] = "00FF00"
    color["Blue"] = "0000FF"
    color["Orange"] = "FF5500"
    color["Purple"] = "8000FF"
    color["Black"] = "000000"
    color["White"] = "FFFFFF"

    return color

def output_fantasy_results(results, players, teams):
    # currently assuming results take format of final_results from fantasy_spreadsheet_io (i.e. a dict of tuples with
    # 2 dicts: starting players and relevant scores, and sub players with relevant scores
    # if we want to fill the sheet with all the stats used to find scores, we can expand that functionality later
    # additionally assuming players and teams take the form of scraped player and team data
    wb = openpyxl.Workbook()
    dest_filename = 'fantasy_book.xlsx'

    ws1 = wb.active
    ws1.title = "Test 2019 Week 2 Results"

    # style setup below
    # colors for styling
    color = name_colors()
    # generic fonts and other things that are regularly reused
    base_font = openpyxl.styles.Font(name='Arial', size=10)
    bold_font = openpyxl.styles.Font(name='Arial', size=10, bold=True)
    big_font = openpyxl.styles.Font(name='Arial', size=14, bold=True)
    name_font = openpyxl.styles.Font(name='Arial', size=14, bold=True, italic=True, color=color["White"])
    bordered = openpyxl.styles.Border(left=openpyxl.styles.Side(border_style='thin'),
                                    right=openpyxl.styles.Side(border_style='thin'),
                                    top=openpyxl.styles.Side(border_style='thin'),
                                    bottom=openpyxl.styles.Side(border_style='thin'))
    # cell backgrounds: must be defined in-loop due to reliance on players' chosen colors
    # cell borders
    # the rows written to are relative to the number of players in the game
    # we can get these from looping through results
    row = 1
    # top row gives the name of the winner in a special message format
    # to get the winner, compare scores of all members of results, the key with highscore wins
    # TODO: deal with ties
    winner = None
    win_color = list()
    for name in results:
        if winner is None or results[name][4] > results[winner][4]:
            winner = name
            win_color = results[name][3]
    # begin by merging top cells
    ws1.merge_cells('B'+str(row)+':F'+str(row))
    winner_cell = ws1['B'+str(row)]
    winner_cell.value = "#" + winner +"Win"
    # special styling for the header
    winner_cell.font = openpyxl.styles.Font(name='Arial', size=24, bold=True, italic=True, color=color[win_color])

    row += 1
    for name in results:
        print(name)
        ws1.merge_cells('A' + str(row) + ':L'+str(row))
        name_cell = ws1['A'+str(row)]
        name_cell.value = name
        # special styling for name cell
        name_cell.font = name_font
        name_cell.fill = openpyxl.styles.PatternFill(fgColor=color[results[name][3]], fill_type='solid')
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
        # week total label
        ws1['L' + str(row)] = "Week Total"
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
        row += 1

        # week totals in this row
        ws1['L' + str(row)] = results[name][4]

        # because sub dict uses weird entries, i think i need to loop through
        # should be inexpensive, just 2 per
        sub_num = 1
        for sub in results[name][1]:
            sub_name = results[name][1][sub][0]
            ws1['A' + str(row)] = "Sub-"+str(sub_num)
            ws1['B' + str(row)] = sub_name
            ws1['C' + str(row)] = players[sub_name][0]
            ws1['D' + str(row)] = players[sub_name][1]
            ws1['E' + str(row)] = players[sub_name][2]
            ws1['F' + str(row)] = players[sub_name][3]
            ws1['G' + str(row)] = results[name][1][sub][1]
            row += 1
            sub_num += 1
        row += 1

    wb.save(dest_filename)

if __name__ == "__main__":
    output_fantasy_results("foobar", "o", "o")