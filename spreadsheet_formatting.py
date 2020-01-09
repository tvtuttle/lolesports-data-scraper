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
    start = 1
    for name in results:
        print(name)
        ws1['A'+str(start)] = name
        start += 1




    wb.save(dest_filename)

if __name__ == "__main__":
    output_fantasy_results("foobar", "o", "o")