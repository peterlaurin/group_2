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

AFFILIATIONS = ['university', 'université', 'universität', 'ucla', 'universidad', 'univ', 'università']

def go(num_pages_to_crawl):
    '''
    Crawl the PLOS One and generate a database. Automatically samples even
    number of articles from each subject area based on num_pages_to_crawl.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl

    Outputs:
        dictionary mapping author identifiers to list of variables
    '''
    #create_sql_database("PLOS_One.db") #can only be run once
    urls_visited = set()
    starting_url = ("https://journals.plos.org/plosone/browse")
    limiting_domain = "journals.plos.org"
    article_absolute_url = 'https://journals.plos.org/plosone/'
    
    subject_urls_lst = get_PLOS_subject_urls(starting_url) #add in limiting_domain?

    #iterate through subject areas
    #for loop counting max urls per subject to crawl
    #get all urls from page function => add to queue
    max_pages_per_subject = math.floor(num_pages_to_crawl / 11)
    for subject_url in subject_urls_lst:
        field = get_field(subject_url)
        subject_soup = get_soup_object(subject_url)
        current_url = subject_url
        urls_visited.add(current_url)
        for _ in range(max_pages_per_subject):
            soup_article_lst = subject_soup.find_all("h2", class_="title")
            for soup_article in soup_article_lst:
                article_url = util.convert_if_relative_url(current_url, soup_article.find_all("a")[0]["href"])
                if article_url not in urls_visited: #util.is_url_ok_to_follow(article_url, limiting_domain)
                    urls_visited.add(article_url)
                    process_article(article_url, field)#process page function
            current_url = get_next_page(subject_soup, subject_url) #function to find next page url
            if not current_url:
                break
            subject_soup = get_soup_object(current_url)
            urls_visited.add(current_url)
    return urls_visited

#c.execute('INSERT INTO AUTHORS (first_name, last_name, institution, field) VALUES (?, ?, ?, ?)', ('bob', 'smith', 'univ', 'field'))    
def get_field(subject_url):
    """
    Finds the associated field from Nature based on PLOS One field.

    Input: 
        subject_url (string)
    Returns:
        field (string)
    """
    PLOS_field = subject_url.split('/')[-1]
    if PLOS_field == 'biology_and_life_sciences':
        field = 'Biological Sciences'
    elif PLOS_field == 'computer_and_information_sciences':
        field = 'Business and Commerce'
    elif PLOS_field == 'earth_sciences' or PLOS_field == 'ecology_and_environmental_sciences':
        field = 'Earth and Environmental Sciences'
    elif PLOS_field == 'engineering_and_technology' or PLOS_field == 'physical_sciences':
        field = 'Physical Sciences'
    elif PLOS_field == 'medicine_and_health_sciences':
        field = 'Health Sciences'
    elif PLOS_field == 'people_and_places' or PLOS_field == 'social_sciences':
        field = 'Social Science'
    else:
        field = 'Scientific Community and Society'

    return field
 

def process_article(article_url, field):
    """
    First table: Authors
Author identifier
First name
Last name
Institution 

paper key paper title year Journal field of study Number of authors


    """
    conn = sqlite3.connect("PLOS_One.db")
    c = conn.cursor()
    authors_table = []
    article_soup = get_soup_object(article_url)
    meta_name_soup = article_soup.find_all("meta", attrs={'name':'citation_author'})
    meta_institution_soup = article_soup.find_all("meta", attrs={'name':'citation_author_institution'})

    
    for i, author_soup in enumerate(meta_name_soup):
        entry = tuple()
        author_name = author_soup["content"]
        names = author_name.split()
        first_name = ''
        for name in names[:-1]:
            first_name += name + " "
        first_name = first_name.strip()
        last_name = names[-1]

        inst_strings = meta_institution_soup[i]["content"] #out of index error
        inst_strings = inst_strings.split(",")
        institution = ''
        for inst_string in inst_strings:
            lower_inst_string = inst_string.lower()
            for affiliation_word in AFFILIATIONS:
                if affiliation_word in lower_inst_string:
                    institution = lower_inst_string
                    break
            
        entry += (first_name, last_name, institution)
        print(entry)
        c.execute('INSERT INTO AUTHORS (first_name, last_name, institution) VALUES (?, ?, ?)', entry)
    c.commit()
#c.execute('INSERT INTO AUTHORS (first_name, last_name, institution) VALUES (?, ?, ?)', ('bob', 'smith', 'univ'))


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

    next_page_url = soup_object.find_all("a", id="nextPageLink")
    if next_page_url:
        next_page_url = next_page_url[0]["href"]
        next_page_url = util.convert_if_relative_url(current_url, next_page_url)
        return next_page_url
    else:
        return None

    

    return next_page_url


def get_PLOS_subject_urls(starting_url):
    """
    Parses the PLOS starting url and extracts the
    urls for each subject area.

    Inputs:
        starting_url (string)

    Returns:
        list of urls for each subject area in PLOS
    
    """
    soup = get_soup_object(starting_url)
    soup_dropdown_menu_lst = soup.find_all("ul", typeof="v:Breadcrumb")
    soup_subject_urls_lst = soup_dropdown_menu_lst[0].find_all("a")
    subject_urls_lst = []
    for a_tag in soup_subject_urls_lst[1:]:
        url = util.convert_if_relative_url(starting_url, a_tag["href"])
        subject_urls_lst.append(url)

    return subject_urls_lst

def get_soup_object(url):
    """
    Takes a url, checks for possible redirection,
    returns soup object.

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
    c.execute('''CREATE TABLE AUTHORS ([author_identifier] INTEGER PRIMARY KEY, [first_name] text, [last_name] text, [institution] text)''')
    c.execute('''CREATE TABLE PAPERS ([paper_identifier] INTEGER PRIMARY KEY, [title] text, [year] text, [journal] text, [field] text, [num_authors] integer)''')
    c.execute('''CREATE TABLE AUTHOR_KEY_RANK ([author_identifier] integer, [paper_identifier] integer, [rank] integer)''')
    conn.commit()

    #c.execute('INSERT INTO AUTHORS (first_name, last_name, institution) VALUES (?, ?, ?)', ('bob', 'smith', 'univ'))




