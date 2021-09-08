from scrape import *


def scrape_mako():
    site_name = "mako"
    site_home = "https://www.n12.co.il/"
    site_proof = "mako.co"
    path_scrape_list = ".\\Websites\\Mako\\mako_category_list.txt"
    path_already_scraped = ".\\Websites\\Mako\\mako_articles_organized.txt"
    path_write_articles = ".\\Websites\\Mako\\mako_articles_raw.txt"
    path_log_errors = ".\\Error Logs\\log.txt"
    scrape_keyword = "Article"
    scrape_remove_characters = ' /"""''()~!@#$%^&*()[]{}<>,.'
    scrape_remove_ending = "#autoplay"

    #  initialize
    create_scrape_list(path_scrape_list, site_home, site_name)
    list_scrape_links = open_scrape_list(path_scrape_list)
    list_scraped_articles = open_scraped_articles(path_already_scraped)
    #  get all articles from the website
    with open(path_write_articles, "w", encoding="utf-8") as f:
        for category in list_scrape_links:
            time.sleep(0.1)
            print("===================================")
            print(category)
            try:
                site = requests.get(category)
            except Exception as e:
                with open(path_log_errors, "a", encoding="utf-8") as errorFile:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    errorFile.write(dt_string, e + '\n')
                    print(e)

            print(site)
            soup = bs4.BeautifulSoup(site.text, 'html.parser')
            for link_tag in soup.find_all('a'):
                link = link_tag.get('href')

                if link is None:
                    continue
                if len(link) > 300 or "javascript" in link:
                    continue
                if link[:5] != "https":
                    link = "https://www.mako.co.il/" + link
                if site_proof not in link[:30]:
                    continue


                if scrape_keyword in link:
                    link = link.strip(scrape_remove_characters)
                    if scrape_remove_ending in link:
                        link = link[:-len(scrape_remove_ending)]
                    if link not in list_scraped_articles:
                        print(link)
                        f.write(link + '\n')
    #  organize the articles
    organize_articles(path_write_articles, list_scraped_articles, path_already_scraped)
    #  extract data
    list_scrape_data = open_scraped_articles(path_already_scraped)
    print(list_scrape_data)
    scrape_article(path_already_scraped, path_log_errors)

