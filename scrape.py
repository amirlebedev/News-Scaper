import requests
import bs4
import time
from database import *


def create_scrape_list(file_path, home_page, site_name):
    #  function creates a list of links to scrape articles from
    list_links = []

    with open(file_path, "w", encoding="utf-8") as f:
        site = requests.get(home_page)
        soup = bs4.BeautifulSoup(site.text, 'html.parser')
        for link_tag in soup.find_all('a'):
            link = link_tag.get('href')
            soup = bs4.BeautifulSoup(site.text, 'html.parser')
            for link_tag in soup.find_all('a'):
                link = link_tag.get('href')
                if link is None:  # check if link exists to prevent errors
                    continue
                if 'https' not in link or site_name not in link:  # check legality of link
                    continue
                if link in list_links:  # check if link already written
                    continue

                print(link)
                list_links.append(link)
                f.write(link + '\n')


def open_scrape_list(file_path):
    #  get the main pages to scrape
    all_links = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            all_links.append(stripped_line)

        print("Main Categories")
        print(all_links)

    return all_links


def open_scraped_articles(file_path):
    #  get the articles already scraped
    with open(file_path, "r", encoding="utf-8") as f:
        list_scraped_articles = []
        for link in f:
            list_scraped_articles.append(link.strip())
        print("Articles Already Scraped")
        print(list_scraped_articles)

    return list_scraped_articles


def get_articles(file_path, all_links, list_scraped_articles,
                 keyword, garbage_letters, ending, error_path, site_proof):
    #  get all the articles on the site
    with open(file_path, "w", encoding="utf-8") as f:
        for category in all_links:
            time.sleep(0.1)
            print("===================================")
            print(category)
            try:
                site = requests.get(category)
            except Exception as e:
                with open(error_path, "a", encoding="utf-8") as errorFile:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    errorFile.write(dt_string + str(e) + '\n')
                    print(e)

            print(site)
            soup = bs4.BeautifulSoup(site.text, 'html.parser')
            for link_tag in soup.find_all('a'):
                link = link_tag.get('href')

                if link is None:
                    continue
                if 'https' not in link or link[:5] != "https" or "javascript" in link:
                    continue
                if len(link) > 300 or site_proof not in link[:30]:
                    continue


                if keyword in link:
                    link = link.strip(garbage_letters)
                    if ending in link:
                        link = link[:-len(ending)]
                    if link not in list_scraped_articles:
                        print(link)
                        f.write(link + '\n')


def organize_articles(path_raw, list_scraped_articles, path_already_scraped):
    #  organize the links and delete duplicates
    #  first we put all links in a list
    with open(path_raw, "r", encoding="utf-8") as f:
        link_list_raw = []
        for line in f:
            link = line.strip()
            link_list_raw.append(link)

    print("List of articltes RAW:")
    print(link_list_raw)

    #  next we remove duplicate article link in the list
    #  find dupes
    index = 1
    list_index_pop = []
    for link in link_list_raw:
        for i in range(index, len(link_list_raw)):
            if link in link_list_raw[i] and i not in list_index_pop:
                list_index_pop.append(i)
        index += 1

    print("List of indexes:")
    print(list_index_pop)

    #  replace dupes with 'REMOVE'
    list_link_remove = link_list_raw[:]
    for i in list_index_pop:
        list_link_remove[i] = 'REMOVE'

    print("Filter list:")
    print(list_link_remove)

    #  remove the REMOVE from the list
    list_organized = []
    for link in list_link_remove:
        if link != 'REMOVE':
            list_organized.append(link)

    print("List of new articles:")
    print(list_organized)

    #  thirdly we write the organized list into a new file
    with open(path_already_scraped, "a", encoding="utf-8") as f:
        for link in list_organized:
            if link not in list_scraped_articles:
                f.write(link + "\n")


def get_metadata(html, get_site_name=True, get_title=True,
                 get_tags=True, get_author=True, get_date=True):

    metadata = ["site", "title", "url", "time", "author", "tags", "time_scraped", "archive_link"]
    tags = []
    for tag in html.find_all("meta"):
        if tag.get("property") == "og:site_name" and get_site_name == True:
            metadata[0] = tag.get("content")
        if tag.get("property") == "og:title" and get_title == True:
            print(tag.get("content").strip("\n").replace("|", " "))
            metadata[1] = tag.get("content").strip("\n").replace("|", " ")
        if tag.get("property") == "article:published_time" and get_date == True:
            metadata[3] = tag.get("content")
        if tag.get("property") == "vr:author" and get_author == True:
            metadata[4] = tag.get("content")
        if tag.get("property") == "article:tag" and get_tags == True:
            metadata[5] = tag.get("content")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        metadata[6] = dt_string
    return metadata


def scrape_article(file_path, error_path):
    #  get the metadata from an article
    #  first we open our main database
    links_database = get_database_links_from_file()

    #  next we get all our articles from file
    links_to_scrape = []
    with open(file_path, "r", encoding="utf-8") as f:
        for link in f:
            links_to_scrape.append(link.strip())

    print("site urls:")
    print(links_to_scrape)

    #  now we check if the article is in the database and scrape every article for metadata
    for link in links_to_scrape:
        if link not in links_database:
            time.sleep(0.1)
            print("===================================")
            print(link)
            try:
                site = requests.get(link)
            except Exception as e:
                with open(error_path, "a", encoding="utf-8") as errorFile:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    errorFile.write(dt_string + ', ' + str(e) + '\n')
                    print(e)
                    continue

            soup = bs4.BeautifulSoup(site.text, "html.parser")
            metadata = get_metadata(soup)
            metadata[2] = link
            metadata_string = convert_list_to_database_format(metadata)
            with open("database.txt", "a", encoding="utf-8") as f:
                f.write(metadata_string)







