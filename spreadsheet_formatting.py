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
    color["Yellow"] = "CCCC00"

    return color


def output_fantasy_results(dest_filename, title, results, players, teams):
    # currently assuming results take format of final_results from fantasy_spreadsheet_io (i.e. a dict of tuples with
    # 2 dicts: starting players and relevant scores, and sub players with relevant scores
    # if we want to fill the sheet with all the stats used to find scores, we can expand that functionality later
    # additionally assuming players and teams take the form of scraped player and team data
    wb = openpyxl.Workbook()
    # dest_filename = 'fantasy_book.xlsx'

    ws1 = wb.active
    ws1.title = title

    # style setup below
    # colors for styling
    color = name_colors()
    # generic , oft-reused styles
    base_style = openpyxl.styles.NamedStyle(name="base_style")
    base_style.font = openpyxl.styles.Font(name='Arial', size=10)
    base_style.alignment = openpyxl.styles.Alignment(horizontal='left')

    bold_style = openpyxl.styles.NamedStyle(name="bold_style")
    bold_style.font = openpyxl.styles.Font(name='Arial', size=10, bold=True)
    bold_style.alignment = openpyxl.styles.Alignment(horizontal='center')

    # stat boxes have borders
    stat_style = openpyxl.styles.NamedStyle(name="stat_style")
    stat_style.font = openpyxl.styles.Font(name='Arial', size=10)
    stat_style.alignment = openpyxl.styles.Alignment(horizontal='right')
    stat_style.border = openpyxl.styles.Border(left=openpyxl.styles.Side(border_style='thin'),
                                               right=openpyxl.styles.Side(border_style='thin'),
                                               top=openpyxl.styles.Side(border_style='thin'),
                                               bottom=openpyxl.styles.Side(border_style='thin'))

    # team stat boxes do NOT have borders
    tstat_style = openpyxl.styles.NamedStyle(name="tstat_style")
    tstat_style.font = openpyxl.styles.Font(name='Arial', size=10)
    tstat_style.alignment = openpyxl.styles.Alignment(horizontal='right')

    name_style = openpyxl.styles.NamedStyle(name="name_style")
    name_style.font = openpyxl.styles.Font(name='Arial', size=14, bold=True, italic=True, color=color["White"])
    # cell backgrounds: must be defined in-loop due to reliance on players' chosen colors

    # column formatting so that the sheet looks nice
    ws1.column_dimensions['A'].width = 15
    ws1.column_dimensions['B'].width = 20
    ws1.column_dimensions['C'].width = 15
    ws1.column_dimensions['D'].width = 15
    ws1.column_dimensions['E'].width = 15
    ws1.column_dimensions['F'].width = 15
    ws1.column_dimensions['G'].width = 15
    ws1.column_dimensions['H'].width = 15
    ws1.column_dimensions['I'].width = 15
    ws1.column_dimensions['J'].width = 15

    # the rows written to are relative to the number of players in the game
    # we can get these from looping through results
    row = 1
    # top row gives the name of the winner in a special message format
    # to get the winner, compare scores of all members of results, the key with highscore wins
    winner = list()
    win_color = list()
    for name in results:
        if len(winner) == 0 or results[name][4] > results[winner[0]][4]:
            winner = [name]
            win_color = [results[name][3]]
        elif results[name][4] == results[winner[0]][4]:
            winner.append(name)
            win_color.append(results[name][3])
    # begin by merging top cells
    ws1.merge_cells('B'+str(row)+':F'+str(row))
    winner_cell = ws1['B'+str(row)]
    winner_string = "#"
    for i in range(len(winner)):
        winner_string += winner[i]
    winner_cell.value = winner_string +"Win"
    # special styling for the header
    winner_cell.alignment = openpyxl.styles.Alignment(horizontal = "center")
    if (len(win_color) == 1):
        winner_cell.font = openpyxl.styles.Font(name='Arial', size=24, bold=True, italic=True, color=color[win_color[0]])
    else:
        winner_cell.font = openpyxl.styles.Font(name='Arial', size=24, bold=True, italic=True, color=color["Black"])

    row += 1
    for name in results:
        # print(name)
        ws1.merge_cells('A' + str(row) + ':H'+str(row))
        name_cell = ws1['A'+str(row)]
        name_cell.value = name
        # special styling for name cell
        name_cell.style = name_style
        name_cell.fill = openpyxl.styles.PatternFill(fgColor=color[results[name][3]], fill_type='solid')
        # after name, 2 cells merged to present score
        ws1.merge_cells('I'+str(row) + ':J' + str(row))
        score_cell = ws1['I' + str(row)]
        score_cell.value = results[name][4]
        score_cell.style = name_style
        score_cell.alignment = openpyxl.styles.Alignment(horizontal='right')
        score_cell.fill = openpyxl.styles.PatternFill(fgColor=color[results[name][3]], fill_type='solid')
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
        # apply formatting to each cell
        ws1['C' + str(row)].style = bold_style
        ws1['D' + str(row)].style = 'bold_style'
        ws1['E' + str(row)].style = 'bold_style'
        ws1['F' + str(row)].style = 'bold_style'
        ws1['G' + str(row)].style = 'bold_style'
        ws1['H' + str(row)].style = 'bold_style'
        ws1['J' + str(row)].style = 'bold_style'

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
        # apply formatting to each cell
        ws1['A' + str(row)].style = 'bold_style'
        ws1['B' + str(row)].style = base_style
        ws1['C'+str(row)].style = tstat_style
        ws1['D' + str(row)].style = 'tstat_style'
        ws1['E' + str(row)].style = 'tstat_style'
        ws1['F' + str(row)].style = 'tstat_style'
        ws1['G' + str(row)].style = 'tstat_style'
        ws1['H' + str(row)].style = 'tstat_style'
        ws1['J' + str(row)].style = 'tstat_style'
        row += 1

        # player stat headers
        ws1['C' + str(row)] = "Kills"
        ws1['D' + str(row)] = "Deaths"
        ws1['E' + str(row)] = "Assists"
        ws1['F' + str(row)] = "CS"
        ws1['G' + str(row)] = "Totals"
        # apply formatting
        ws1['C' + str(row)].style = 'bold_style'
        ws1['D' + str(row)].style = 'bold_style'
        ws1['E' + str(row)].style = 'bold_style'
        ws1['F' + str(row)].style = 'bold_style'
        ws1['G' + str(row)].style = 'bold_style'

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
        # apply formatting
        ws1['A'+str(row)].style = 'bold_style'
        ws1['B' + str(row)].style = 'base_style'
        ws1['C' + str(row)].style = stat_style
        ws1['D' + str(row)].style = 'stat_style'
        ws1['E' + str(row)].style = 'stat_style'
        ws1['F' + str(row)].style = 'stat_style'
        ws1['G' + str(row)].style = 'stat_style'

        row += 1

        ws1['A' + str(row)] = "Jungle"
        jung = results[name][0][2][0]
        ws1['B' + str(row)] = jung
        ws1['C' + str(row)] = players[jung][0]
        ws1['D' + str(row)] = players[jung][1]
        ws1['E' + str(row)] = players[jung][2]
        ws1['F' + str(row)] = players[jung][3]
        ws1['G' + str(row)] = results[name][0][2][1]
        # apply formatting
        ws1['A' + str(row)].style = 'bold_style'
        ws1['B' + str(row)].style = 'base_style'
        ws1['C' + str(row)].style = 'stat_style'
        ws1['D' + str(row)].style = 'stat_style'
        ws1['E' + str(row)].style = 'stat_style'
        ws1['F' + str(row)].style = 'stat_style'
        ws1['G' + str(row)].style = 'stat_style'

        row += 1

        ws1['A' + str(row)] = "Mid"
        mid = results[name][0][3][0]
        ws1['B' + str(row)] = mid
        ws1['C' + str(row)] = players[mid][0]
        ws1['D' + str(row)] = players[mid][1]
        ws1['E' + str(row)] = players[mid][2]
        ws1['F' + str(row)] = players[mid][3]
        ws1['G' + str(row)] = results[name][0][3][1]
        # apply formatting
        ws1['A' + str(row)].style = 'bold_style'
        ws1['B' + str(row)].style = 'base_style'
        ws1['C' + str(row)].style = 'stat_style'
        ws1['D' + str(row)].style = 'stat_style'
        ws1['E' + str(row)].style = 'stat_style'
        ws1['F' + str(row)].style = 'stat_style'
        ws1['G' + str(row)].style = 'stat_style'

        row += 1

        ws1['A' + str(row)] = "Bot"
        bot = results[name][0][4][0]
        ws1['B' + str(row)] = bot
        ws1['C' + str(row)] = players[bot][0]
        ws1['D' + str(row)] = players[bot][1]
        ws1['E' + str(row)] = players[bot][2]
        ws1['F' + str(row)] = players[bot][3]
        ws1['G' + str(row)] = results[name][0][4][1]
        # apply formatting
        ws1['A' + str(row)].style = 'bold_style'
        ws1['B' + str(row)].style = 'base_style'
        ws1['C' + str(row)].style = 'stat_style'
        ws1['D' + str(row)].style = 'stat_style'
        ws1['E' + str(row)].style = 'stat_style'
        ws1['F' + str(row)].style = 'stat_style'
        ws1['G' + str(row)].style = 'stat_style'

        row += 1

        ws1['A' + str(row)] = "Support"
        supp = results[name][0][0][0]
        ws1['B' + str(row)] = supp
        ws1['C' + str(row)] = players[supp][0]
        ws1['D' + str(row)] = players[supp][1]
        ws1['E' + str(row)] = players[supp][2]
        ws1['F' + str(row)] = players[supp][3]
        ws1['G' + str(row)] = results[name][0][0][1]
        # apply formatting
        ws1['A' + str(row)].style = 'bold_style'
        ws1['B' + str(row)].style = 'base_style'
        ws1['C' + str(row)].style = 'stat_style'
        ws1['D' + str(row)].style = 'stat_style'
        ws1['E' + str(row)].style = 'stat_style'
        ws1['F' + str(row)].style = 'stat_style'
        ws1['G' + str(row)].style = 'stat_style'

        row += 1

        # because sub dict uses weird entries, i think i need to loop through
        # should be inexpensive, just 2 per
        #todo: alter due to change from sub dict to sub list of tuples
        sub_num = 1
        for sub in results[name][1]:
            # sub_name = results[name][1][sub][0]
            sub_name = sub[0]
            ws1['A' + str(row)] = "Sub-"+str(sub_num)
            ws1['B' + str(row)] = sub_name
            ws1['C' + str(row)] = players[sub_name][0]
            ws1['D' + str(row)] = players[sub_name][1]
            ws1['E' + str(row)] = players[sub_name][2]
            ws1['F' + str(row)] = players[sub_name][3]
            # ws1['G' + str(row)] = results[name][1][sub][1]
            ws1['G' + str(row)] = sub[1]
            # apply formatting
            ws1['A' + str(row)].style = 'bold_style'
            ws1['B' + str(row)].style = 'base_style'
            ws1['C' + str(row)].style = 'stat_style'
            ws1['D' + str(row)].style = 'stat_style'
            ws1['E' + str(row)].style = 'stat_style'
            ws1['F' + str(row)].style = 'stat_style'
            ws1['G' + str(row)].style = 'stat_style'

            row += 1
            sub_num += 1
        row += 1

    wb.save(dest_filename)

