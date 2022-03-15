import PySimpleGUI as sg
from ynet import *
from archive import *


# Define the window's contents
layout = [[sg.Text("Select the news websites:")],
          [sg.Checkbox('Ynet', default=True, key="-YNET-")],
          [sg.Checkbox('Mako', default=False, key="-MAKO-")],
          [sg.Checkbox('Walla (not recommended)', default=False, key="-WALLA-")],
          [sg.Text("Select action:")],
          [sg.Checkbox('Get articles from the web', default=True, key="-ARTICLES-")],
          [sg.Checkbox('Archive articles,', default=True, key="-ARCHIVE-"), sg.Text('Starting line number:'), sg.Input(key='-INPUT-', default_text="0")],
          [sg.Button('Run'), sg.Button('Quit')]]

# Create the window
window = sg.Window('News Scraper GUI',  layout, size=(400, 250))

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Running the program
    elif event == "Run":
        scraping_articles = values['-YNET-'] == True or values['-MAKO-'] == True or values['-WALLA-'] == True
        if values["-ARTICLES-"] == True and scraping_articles == True:
            print("################")
            print("##--SCRAPING--##")
            print("###############")

            if values["-YNET-"] == True:
                scrape_ynet()
            if values["-MAKO-"] == True:
                scrape_mako()
            if values["-WALLA-"] == True:
                scrape_walla()

        if values["-ARCHIVE-"] == True:
            print("################")
            print("##-ARCHIVING-##")
            print("###############")

            line_counter = int(values['-INPUT-'])
            archive_database(line_counter)

        # break out of GUI
        break

# Finish up by removing GUI from the screen
print("DONE")
window.close()
