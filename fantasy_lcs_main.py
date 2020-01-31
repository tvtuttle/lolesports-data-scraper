# this file will act as the true main eventually
# want to include ui or user input prompts to make program easily useable, esp. outside ide
# will prompt user (in some way) for information, then send that info to spreadsheet io
# for now, focus on command line input w/ input function

from fantasy_spreadsheet_io import play_fantasy

if __name__ == "__main__":
    # prompt for user input
    league = input("Welcome to Fantasy LCS. Please choose a league (LCS, LEC): ")
    league = league.upper()
    while league not in ['LCS', 'LEC']:
        league = input("Invalid league. Please select a supported league (LCS, LEC): ")
        league = league.upper()

    year = input("Please choose a year (ex. 2019): ")
    while year not in ['2018', '2019', '2020', '2021']: #TODO make this and other checks more robust
        year = input("Invalid year. Please select a supported year (2019, 2020): ")

    season = input("Please choose a season (Spring, Summer): ")
    season = season.lower()
    season = season.capitalize()
    while season not in ['Spring', 'Summer']:
        season = input("Invalid season. Please select a supported season (Spring, Summer): ")
        season = season.lower()
        season = season.capitalize()
    week = input("Please choose a week number: ")
    while int(week) not in range(1, 10):
        week = input("Invalid number. Please select a supported week (1 through 9): ")

    # this could be better secured
    input_path = input("Please enter the location of your fantasy team data: ")
    output_path = input("Please enter the preferred output location of your fantasy team results: ")

    title = (league + " " + year + " " + season + ", Week " + week)
    # print(title)
    # generate url based on input
    # this is reliant on leaguepedia maintaining consistent url naming guidelines
    url = "https://lol.gamepedia.com/" + league + "/" + year + "_Season/" + season + "_Season/Scoreboards"
    if week != '1':
        url += "/Week " + week
    print("Scoreboard URL: " + url)
    play_fantasy(input_path, url, title, output_path)
    print("Done!")

