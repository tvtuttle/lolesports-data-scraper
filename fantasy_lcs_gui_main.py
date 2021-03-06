# a replacement for fantasy_lcs_main, uses a tkinter gui instead of command line input
# currently only support windows, due to os.startfile function
#TODO handle inputs with try/except statements, esp. for ifile and ofile

import tkinter as tk
import tkinter.filedialog as fd
import os
from fantasy_spreadsheet_io import play_fantasy

# global file variables
ifile = None
ifile_name = None

ofile = None
ofile_name = None


# functions called by buttons
def openfile():
    global ifile
    global ifile_name
    ifile = fd.askopenfile(mode='r')
    ifile_name.set(ifile.name)


# expects string input
def buildurl(l, y, s, w):
    url = "https://lol.gamepedia.com/" + l + "/" + y + "_Season/" + s + "_Season/Scoreboards"
    if w != '1':
        url += "/Week " + w
    return url


def buildtitle(l, y, s, w):
    title = (l + " " + y + " " + s + ", Week " + w)
    return title


# main
if __name__ == "__main__":
    # create window
    m = tk.Tk()
    m.title("Fantasy LCS")

    # league selection
    league_frame = tk.Frame(m)
    league_frame.pack()

    league_label = tk.Label(league_frame, text="League:")
    league_label.pack(side="left")

    league = tk.StringVar()
    league.set("LCS")  # default value
    lcs_button = tk.Radiobutton(league_frame, text="LCS", variable=league, value="LCS")
    lcs_button.pack(side="left")
    lec_button = tk.Radiobutton(league_frame, text="LEC", variable=league, value="LEC")
    lec_button.pack(side="left")

    # season selection
    year_frame = tk.Frame(m)
    year_frame.pack()

    year_label = tk.Label(year_frame, text="Year:")
    year_label.pack(side="left")

    year = tk.IntVar()
    year.set(2020)  # default value
    season = tk.StringVar()
    season.set("Spring")
    year_menu = tk.Menubutton(year_frame, relief="raised", textvariable=year)
    year_menu.menu = tk.Menu(year_menu, tearoff=0)
    year_menu["menu"] = year_menu.menu
    year_menu.menu.add_checkbutton(label="2019", variable=year, onvalue=2019)
    year_menu.menu.add_checkbutton(label="2020", variable=year, onvalue=2020)
    year_menu.pack(side="left")
    season_menu = tk.Menubutton(year_frame, relief="raised", textvariable=season)
    season_menu.menu = tk.Menu(season_menu, tearoff=0)
    season_menu["menu"] = season_menu.menu
    season_menu.menu.add_checkbutton(label="Spring", variable=season, onvalue="Spring")
    season_menu.menu.add_checkbutton(label="Summer", variable=season, onvalue="Summer")
    season_menu.pack(side="left")

    # week selection
    week = tk.IntVar()
    week.set(1)
    week_frame = tk.Frame(m)
    week_frame.pack()

    week_label = tk.Label(week_frame, text="Week:")
    week_label.pack(side="left")

    week_menu = tk.Menubutton(week_frame, relief="raised", textvariable=week)
    week_menu.menu = tk.Menu(week_menu, tearoff=0)
    week_menu["menu"] = week_menu.menu
    for i in range(1, 10):
        week_menu.menu.add_checkbutton(label=str(i), variable=week, onvalue=i)
    week_menu.pack(side="left")

    # input file selection
    ifile_frame = tk.Frame(m)
    ifile_frame.pack()

    ifile_label = tk.Label(ifile_frame, text="Input CSV:")
    ifile_label.pack(side="left")

    ifile_name = tk.StringVar()
    ifile_name.set("Choose file:")
    ifile_button = tk.Button(ifile_frame, command=openfile, textvariable=ifile_name)
    ifile_button.pack(side="left")

    # output file name field (currently, .xlsx must be appended, auto-append not added yet)
    ofile_frame = tk.Frame(m)
    ofile_frame.pack()
    ofile_label = tk.Label(ofile_frame, text="Output Filename:")
    ofile_label.pack(side="left")
    ofile_name = tk.StringVar()
    ofile_name.set("results.xlsx")
    ofile_entry = tk.Entry(ofile_frame, textvariable=ofile_name)
    ofile_entry.pack(side="left")
    # ofile_suffix = tk.Label(ofile_frame, text=".xlsx")
    # ofile_suffix.pack(side="left")

    # before running play_fantasy, must build url from selection menus/radiobuttons
    # url = "https://lol.gamepedia.com/" + league.get() + "/" + str(year.get()) + "_Season/" + season.get() + "_Season/Scoreboards"
    # if week != '1':
    #     url += "/Week " + str(week.get())

    # finally, define title based on variables
    # title = "Lolesports fantasy"
    # run button
    run_frame = tk.Frame(m)
    run_frame.pack()
    print(ifile_name.get())
    # print(url)
    # print(title)
    print(ofile_name.get())
    run_button = tk.Button(run_frame, text="Generate and Open Results", command=lambda: play_fantasy(ifile_name.get(),
                           buildurl(league.get(), str(year.get()), season.get(), str(week.get())),
                           buildtitle(league.get(), str(year.get()), season.get(), str(week.get())), ofile_name.get()))
    run_button.pack(side="left")

    # run gui
    m.mainloop()