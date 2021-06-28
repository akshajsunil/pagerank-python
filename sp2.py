import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import sqlite3


colorama.init()

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS Pages''')
cur.execute('''CREATE TABLE IF NOT EXISTS Pages
    (id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT,
     error INTEGER, old_rank REAL, new_rank REAL)''')

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET


internal_urls = set()
external_urls = set()

total_urls_visited = 0


def is_valid(url):
   
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
  
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")


    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, level,max_urls=50):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    no=0
    links = get_all_website_links(url)
    for link in links:
            if("https://en.wikipedia.org/wiki/" in link and "%" not in link and ":" not in link[30:]):
                no=no+1
                cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( link, ) )
                conn.commit()


    cur.execute('''SELECT new_rank FROM Pages WHERE url = ?''', (url, ))
    row = cur.fetchone()
    if row is None:
        r=1
        nr=r/no
    else:

        nr=row[0]/no
    print(nr)
    for link in links:

        if("https://en.wikipedia.org/wiki/" in link and "%" not in link and ":" not in link[30:]):
            no=no+1
            cur.execute('''SELECT old_rank FROM Pages WHERE url= ?''',(url, ))
            oldra=cur.fetchone()
            if oldra is None or oldra[0] is None:
                m=1
                nera=nr+m
            else:
                nera=nr+oldra[0]

            cur.execute('UPDATE Pages SET old_rank=new_rank,new_rank=? WHERE url=? ', ( nera,link ) )
            conn.commit()

    for link in links:
        if total_urls_visited > max_urls:
            break
        print(str(level)+"-----------------------------------------------------------------------")
        level=level+1
        crawl(link,level,max_urls=max_urls)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)
    
    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls
    level=0
    crawl(url,level,max_urls=max_urls)



    domain_name = urlparse(url).netloc

 
    t=0
    lin=[]
    for internal_link in internal_urls:
        

            
            print(internal_link[30:])


    
