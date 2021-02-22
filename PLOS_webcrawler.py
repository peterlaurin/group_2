# CS122: Final Project
# Web crawler for PLOS website
#
# Lily Mansfield
#

import re
import util
import bs4
import queue
import json
import sys
import csv
import math
import sqlite3

def go(num_pages_to_crawl):
    '''
    Crawl the PLOS One and generate a database. Automatically samples even
    number of articles from each subject area based on num_pages_to_crawl.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl

    Outputs:
        dictionary mapping author identifiers to list of variables
    '''
    urls_visited = set()
    starting_url = ("https://journals.plos.org/plosone/browse")
    limiting_domain = "journals.plos.org"
    
    subject_urls_lst = get_PLOS_subject_urls(starting_url, limiting_domain)

    #iterate through subject areas
    #for loop counting max urls per subject to crawl
    #get all urls from page function => add to queue
    max_urls_per_subject = math.floor(num_pages_to_crawl / 11)
    for subject_url in subject_urls_lst:
        subject_soup = get_soup_object(subject_url)
        current_url = subject_url
        urls_visited.add(current_url)
        for _ in range(max_urls_per_subject):
            soup_article_lst = subject_soup.find_all("h2", class_="title")

            for soup_article in soup_article_lst:
                article_url = util.convert_if_relative_url(current_url, soup_article.find_all("a")[0]["href"])
                if util.is_url_ok_to_follow(article_url, limiting_domain) \
                    and article_url not in urls_visited:
                    urls_visited.add(article_url)
                    #process page function
            current_url = get_next_page(subject_soup, current_url) #function to find next page url
            if not current_url:
                break
            #subject_soup = #
            urls_visited.add(current_url)


    
def process_article(article_url):
    """
    """

def get_next_page(soup_object, current_url):
    """
    Takes a PLOS url page of articles and gets
    the next page

    Inputs:
        current_url (string): url for the Soup object
        soup_object (Soup Object)
    Returns:
        next page url (string)
    """
    #NOT WORKING
    try:
        next_page_url = soup_object.find_all("a", id="nextPageLink")[0]["href"]
        next_page_url = util.convert_if_relative_url(current_url, next_page_url)
        print("hello")
        return next_page_url
    except IndexError as i:
        return None
    

    return next_page_url


def get_PLOS_subject_urls(starting_url):
    """
    Parses the PLOS starting url and extractst the
    urls for each subject area.

    Inputs:
        starting_url (string)

    Returns:
        list of urls for each subject areas in PLOS
    
    """
    soup = get_soup_object(starting_url)
    soup_dropdown_menu_lst = soup.find_all("ul", typeof="v:Breadcrumb")
    soup_subject_urls_lst = soup_dropdown_menu_lst[0].find_all("a")
    subject_urls_lst = []
    for a_tag in soup_subject_urls_lst[1:]:
        url = util.convert_if_relative_url(current_url, a_tag["href"])
        subject_urls_lst.append(url)

    return subject_urls_lst

def get_soup_object(url):
    """
    Takes a url, checks for possible redirection,
    returns soup object

    Inputs:
        url (string)
    
    Returns:
        Soup object
    """
    request = util.get_request(url) 
    html_text = util.read_request(request)
    current_url = util.get_request_url(request)  #gets correct url in case of redirection
    soup = bs4.BeautifulSoup(html_text, 'html5lib')

    return soup

def create_sql_database(database_name):
    """
    Creates the three table schemas for the SQL database: AUTHORS, 
    PAPERS, and AUTHOR_KEY_RANK.
    """
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE AUTHORS ([author_identifier] INTEGER PRIMARY KEY, [first_name] text,
     [last_name] text, [institution] text''')
    c.execute('''CREATE TABLE PAPERS ([paper_identifier] INTEGER PRIMARY KEY, [title] text, 
    [year] text, [journal] text, [field] text, [num_authors] integer)''')
    c.execute('''CREATE TABLE AUTHOR_KEY_RANK ([author_identifier] integer, [paper_identifier] integer, 
    [rank] integer''')
    conn.commit()

    #c.execute('INSERT INTO AUTHORS (first_name, last_name, institution, field) VALUES (?, ?, ?, ?)', ('bob', 'smith', 'univ', 'field'))
def process_webpage(article_url):
    """
    """



