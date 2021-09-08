from scrape import *


def scrape_walla():
    site_name = "walla"
    site_home = "https://www.walla.co.il/"
    site_proof = "walla.co"
    path_scrape_list = ".\\Websites\\Walla\\walla_category_list.txt"
    path_already_scraped = ".\\Websites\\Walla\\walla_articles_organized.txt"
    path_write_articles = ".\\Websites\\Walla\\walla_articles_raw.txt"
    path_log_errors = ".\\Error Logs\\log.txt"
    scrape_keyword = "item"
    scrape_remove_characters = ' /"""''()~!@#$%^&*()[]{}<>,.'
    scrape_remove_ending = "#autoplay"

    #  initialize
    create_scrape_list(path_scrape_list, site_home, site_name)
    list_scrape_links = open_scrape_list(path_scrape_list)
    list_scraped_articles = open_scraped_articles(path_already_scraped)
    #  get all articles from the website
    get_articles(path_write_articles, list_scrape_links,list_scraped_articles,
                 scrape_keyword, scrape_remove_characters, scrape_remove_ending,
                 path_log_errors, site_proof)
    #  organize the articles
    organize_articles(path_write_articles, list_scraped_articles, path_already_scraped)
    #  extract data
    list_scrape_data = open_scraped_articles(path_already_scraped)
    print(list_scrape_data)
    scrape_article(path_already_scraped, path_log_errors)
