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
import gender

AFFILIATIONS = ['university', 'université', 'universität', 'ucla', 'universidad', 'univ', 'università', 'school']

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
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    article_soup = get_soup_object(article_url)
    num_authors = len(article_soup.find_all("meta", attrs = {"name" : "citation_author"}))
    paper_identifier = add_paper_table_entry(article_soup, field, num_authors, conn, c)
    add_authors_table_entry(article_soup, paper_identifier, conn, c)

    conn.close()
"""
    meta_name_soup = article_soup.find_all("meta", attrs={'name':'citation_author'})
    meta_institution_soup = article_soup.find_all("meta", attrs={'name':'citation_author_institution'})

    print(article_url)
    for i, author_soup in enumerate(meta_name_soup):
        entry = tuple()
        author_name = author_soup["content"].split()
        last_name = author_name.pop()
        first_name = ' '.join(author_name)

        inst_strings = meta_institution_soup[i]["content"] #out of index error
        institution = get_institution_name(inst_strings)

        author_gender = gender.get_gender(author_name[0].lower())
        
        entry += (first_name, last_name, institution, author_gender)
        print(entry)
        #c.execute('INSERT INTO AUTHORS (first_name, last_name, institution, gender) VALUES (?, ?, ?, ?)', entry)
        #c.commit()
"""

def add_paper_table_entry(article_soup, field, num_authors, conn, c):
    """
    """
    title = article_soup.find_all("meta", attrs={"name": "citation_title"})[0]["content"]
    date = article_soup.find_all("meta", attrs={"name": "citation_date"})[0]["content"].split()[-1]
    journal = "PLOS One"
    entry = (title, date, journal, field, num_authors)
    c.execute('INSERT INTO papers (title, year, journal, field, num_authors) VALUES (?, ?, ?, ?, ?)', entry)
    conn.commit()

    paper_identifier = c.execute("select paper_identifier from papers where title = ?", (title,)).fetchall()[0][0]
    conn.commit()
    return paper_identifier


def add_authors_table_entry(article_soup, paper_identifier, conn, c):
    """
    """
    num_authors = len(article_soup.find_all("meta", attrs = {"name" : "citation_author"}))
    citation_soup = article_soup.find_all("meta", attrs = {'name':'citation_doi'})[0]
    institution = ""
    authors_added = 0
    entry = tuple()
    author_gender = ""
    find_institution = False
    while authors_added < num_authors:
        citation_soup = citation_soup.nextSibling
        if isinstance(citation_soup, str):#citation_soup.strip() == '\n' or citation_soup == '\n  ':
            continue
        elif citation_soup['name'] == 'citation_author':
            if find_institution:
                entry += ("", author_gender)
                print(entry)
                authors_added += 1
                c.execute('INSERT INTO authors (first_name, last_name, institution, gender) VALUES (?, ?, ?, ?)', entry)
                conn.commit()
                author_identifier = c.execute("select author_identifier from authors where first_name = ? and last_name = ?", (first_name, last_name)).fetchall()[0][0]
                conn.commit()
                rank = authors_added
                c.execute('INSERT INTO author_key_rank (author_identifier, paper_identifier,rank) VALUES (?, ?, ?)', (author_identifier, paper_identifier, rank) )
                conn.commit()
                find_institution = False
                entry = tuple()
            author_name = citation_soup["content"].split()
            last_name = author_name.pop()
            first_name = ' '.join(author_name)
            print(first_name)
            author_gender = gender.get_gender(author_name[0])
            entry += (first_name, last_name)
            find_institution = True
        elif find_institution and citation_soup["name"] == "citation_author_institution":
            institution = get_institution_name(citation_soup)
            if institution:
                entry += (institution.strip(), author_gender)
                print(entry)
                authors_added += 1
                c.execute('INSERT INTO authors (first_name, last_name, institution, gender) VALUES (?, ?, ?, ?)', entry)
                conn.commit()
                author_identifier = c.execute("select author_identifier from authors where first_name = ? and last_name = ?", (first_name, last_name)).fetchall()[0][0]
                conn.commit()
                rank = authors_added
                c.execute('INSERT INTO author_key_rank (author_identifier, paper_identifier,rank) VALUES (?, ?, ?)', (author_identifier, paper_identifier, rank) )
                conn.commit()
                find_institution = False
                print(entry)
                entry = tuple()
                


    

def get_institution_name(citation_soup):
    """
    """
    inst_strings = citation_soup["content"].lower().split(",")
    institution = ''
    for inst_string in inst_strings:
        for affiliation_word in AFFILIATIONS:
            if affiliation_word in inst_string:
                institution = inst_string
                return institution
    
    return ""


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
    c.execute('''CREATE TABLE authors ([author_identifier] INTEGER PRIMARY KEY, [first_name] text, [last_name] text, [institution] text, [gender] text, CONSTRAINT full_name UNIQUE (first_name, last_name))''')
    c.execute('''CREATE TABLE papers ([paper_identifier] INTEGER PRIMARY KEY, [title] text UNIQUE, [year] text, [journal] text, [field] text, [num_authors] integer)''')
    c.execute('''CREATE TABLE author_key_rank ([author_identifier] integer, [paper_identifier] integer, [rank] integer)''')
    conn.commit()

    #c.execute('INSERT INTO AUTHORS (first_name, last_name, institution) VALUES (?, ?, ?)', ('bob', 'smith', 'univ'))




