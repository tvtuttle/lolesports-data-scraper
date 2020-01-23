# lolesports-data-scraper
The goal of this project is to create an easily-implementable Fantasy LCS game and stat tracking system, in lieu of an official Fantasy LCS league.
Fantasy LCS is a game inspired by such other fantasy sports games as fantasy baseball and fantasy football, in which fantasy players create fantasy teams of real sports players and calculate their statistics from real games to determine which fantasy team has the best roster of real players. Fantasy LCS applies this popular fantasy concept to professional League of Legends, one of the most popular "esports" (competitive video games) in the world.
This program, when given a list of fantasy players and the members of their fantasy team (a real team and 7 real players), scrapes the commonly-used and regularly updated Leaguepedia wiki (lol.gamepedia.com) to determine the statistics of the real team and players, then calculates their resulting fantasy scores and returns the results in a formatted spreadsheet.
Currently, the program can be used by running fantasy_lcs_main.py using python. Running this file as main will generate text prompts which can be used to customise input and output.
The program requires a specially formatted csv containing fantasy team details as input, and will output the results to a specially-formated xlsx file with a name specified by user input.

This program was developed for use in Python 3.8.1, and requires packages that can be installed using pip. All necessary packages and their required versions can be found in the requirements.txt file.

The .idea folder in this repository contains setting information specific to the PyCharm IDE, where this project was created. AS FAR AS I KNOW, its presence should not affect the program, which should be runnable by any Python compiler or environment (assuming necessary packages are installed).
