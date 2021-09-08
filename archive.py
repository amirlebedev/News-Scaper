import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from database import *
from scrape import *


def check_archived(url):
    open_archive = "http://archive.org/wayback/available?url=" + url
    try:
        response = requests.get(open_archive)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        api = soup.text
        print(api)
        if '"archived_snapshots": {}}' in api:
            print("NOT ARCHIVED")
            return [False, url]
        elif '"available": true' in api:
            print("YES ARCHIVED")
            response = requests.get("https://web.archive.org/web/" + url)
            print(response.url)
            return [True, response.url]
        else:
            return [False, url]
    except Exception:
        return [False, url]  # error opening the archiver


def archive_database(line_counter):
    database = get_database()
    database_copy = make_database_copy(database)

    # set options for selenium chrome driver
    options = webdriver.ChromeOptions()
    options.headless = True  # make the browser run in the background
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)

    for data in database[line_counter:]:
        if data[7] == "archive_link":  # check if the database contains the archive link
            print("Archiving:", str(line_counter+1) + "/" + str(len(database)), data[0], data[2], data[1])
            #  first we check if the page has already been archived
            url = data[2]
            url_archive = check_archived(url)
            if url_archive[0] == True:
                database_copy[line_counter][7] = url_archive[1]
                write_database(database_copy)
                time.sleep(0.1)
            #  open chromedriver and archive links
            else:
                try:
                    driver.get("https://web.archive.org/save")
                    elem = driver.find_element_by_id('web-save-url-input')
                    elem.send_keys(data[2])
                    elem.send_keys(Keys.ENTER)
                    for i in range(0, 6):
                        print("Waiting range", str(i * 5) + "-" + str((i + 1) * 5), "seconds.")
                        time.sleep(5)
                        try:
                            partial_link = driver.find_element_by_xpath("//a[contains(@href,'/web/')]").text
                            archive_link = "https://web.archive.org/" + partial_link
                            break
                        except Exception as e:
                            continue
                    partial_link = driver.find_element_by_xpath("//a[contains(@href,'/web/')]").text
                    archive_link = "https://web.archive.org/" + partial_link
                    print("Archive link:", archive_link)
                    database_copy[line_counter][7] = archive_link
                    #  update the database
                    write_database(database_copy)
                except Exception:
                    print("Error archiving.")

        line_counter += 1

    driver.close()
    convert_to_html_view()
    write_database_backup(database_copy)
