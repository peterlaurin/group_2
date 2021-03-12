# CS122: Final Project
# Web crawler for PLOS website to scrape authorship and paper data
#
# Lily Mansfield
#
#Calling PLOS_webcrawler.go(num_articles_to_crawl, start_page, database_name) starts the
#crawler. Crawler will print authors table entries, unique errors and (author_identifier, paper_identifier)
#to terminal so user can track progress. 

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

AFFILIATIONS = ['university', 'université', 'universität', 'ucla',\
     'universidad', 'univ', 'università', 'school', 'laboratory']

def go(num_articles_to_crawl, start_page, database_name):
    '''
    Crawl the PLOS One and generate an SQL database. Automatically samples even
    number of articles from each subject area based on num_articles_to_crawl.

    Inputs:
        num_articles_to_crawl (int): theapproximate number of articles to process during the crawl
        start_page (int): page of PLOS One subject browsing to start crawling at
        database_name (string): name of database to add to 
    '''
    urls_visited = set()
    starting_url = ("https://journals.plos.org/plosone/browse")
    subject_urls_lst = get_PLOS_subject_urls(starting_url)  

    num_articles_per_field = num_articles_to_crawl / 11
    num_pages_per_field = math.ceil(num_articles_per_field / 13)
  
    for subject_url in subject_urls_lst:
        field = get_field(subject_url)
        subject_url += '?page=' + str(start_page)
        subject_soup = get_soup_object(subject_url)
        current_url = subject_url
        urls_visited.add(current_url)
        for _ in range(num_pages_per_field):
            soup_article_lst = subject_soup.find_all("h2", class_="title")
            for soup_article in soup_article_lst:
                article_url = util.convert_if_relative_url(current_url, soup_article.find_all("a")[0]["href"])
                if article_url not in urls_visited: 
                    urls_visited.add(article_url)
                    process_article(article_url, field, database_name)
            current_url = get_next_page(subject_soup, subject_url) 
            if not current_url:
                break
            subject_soup = get_soup_object(current_url)
            urls_visited.add(current_url)
    
    return 


def get_field(subject_url):
    """
    Finds the associated field from Nature based on PLOS One field
    (we prioritized Nature subjects categorization).

    Input: 
        subject_url (string)
    Returns:
        field (string)
    """
    PLOS_field = subject_url.split('/')[-1]
    if PLOS_field == 'biology_and_life_sciences':
        field = 'biological-sciences'
    elif PLOS_field == 'computer_and_information_sciences':
        field = 'business-and-commerce'
    elif PLOS_field == 'earth_sciences' or PLOS_field == 'ecology_and_environmental_sciences':
        field = 'earth-and-environmental-sciences'
    elif PLOS_field == 'engineering_and_technology' or PLOS_field == 'physical_sciences':
        field = 'physical-sciences'
    elif PLOS_field == 'medicine_and_health_sciences':
        field = 'health-sciences'
    elif PLOS_field == 'people_and_places' or PLOS_field == 'social_sciences':
        field = 'social-science'
    else:
        field = 'scientific-community-and-society'

    return field
 

def process_article(article_url, field, database_name):
    """
    Processes an article from PLOS_One by adding entries from 
    the article to all three tables (authors, papers and author_paper_rank).

    Inputs:
        article_url (string)
        field (string)
        database_name (string)
    """
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    
    article_soup = get_soup_object(article_url)
    num_authors = len(article_soup.find_all("meta", attrs = {"name" : "citation_author"}))
    paper_identifier = add_paper_table_entry(article_soup, field, num_authors, conn, c)
    try:
        add_authors_table_entry(article_soup, paper_identifier, conn, c)
    except:
        print('error, problem with adding authors')
        conn.close()
        return

    conn.close()


def add_paper_table_entry(article_soup, field, num_authors, conn, c):
    """
    Adds entry to the SQL paper table after retrieving the necesssary values.

    Inputs:
        article_soup (BeautifulSoup Object)
        field (string)
        num_authors (integer)
        conn (sqlite3 connection)
        c (sqlite3 cursor)
    """
    title = article_soup.find_all("meta", attrs={"name": "citation_title"})[0]["content"]
    date = article_soup.find_all("meta", attrs={"name": "citation_date"})[0]["content"].split()[-1]
    journal = "PLOS One"
    entry = (title, date, journal, field, num_authors)
    try:
        c.execute('INSERT INTO papers (title, year, journal, field, num_authors) VALUES (?, ?, ?, ?, ?)',\
             entry)
        conn.commit()
    except:
        print("error, paper insert not unique")

    paper_identifier = c.execute("select paper_identifier from papers where title = ?",\
         (title,)).fetchall()[0][0]
    conn.commit()
    return paper_identifier


def add_authors_table_entry(article_soup, paper_identifier, conn, c):
    """
    Parses article to find (first_name, last_name, institution, gender, country) for entry
    to authors table. Also adds entry to author_key_rank table for each author found.

    Inputs:
        article_soup (BeautifulSoup object)
        paper_identifier (integer)
        conn (sqlite3 connection)
        c (sqlite3 cursor)
    """
    num_authors = len(article_soup.find_all("meta", attrs = {"name" : "citation_author"}))
    citation_soup = article_soup.find_all("meta", attrs = {'name':'citation_doi'})[0]
    institution = ""
    author_gender = ""
    authors_added = 0
    entry = tuple()
    find_institution = False

    while authors_added < num_authors:
        citation_soup = citation_soup.nextSibling
        if isinstance(citation_soup, str) or not isinstance(citation_soup, bs4.element.Tag):
            continue
        elif citation_soup.has_attr("name"):
            if citation_soup['name'] == 'citation_author':
                if find_institution:
                    institution, country = get_institution_name_and_country(None)
                    entry += (institution, author_gender, country)
                    print(entry)
                    authors_added += 1
                    entry = insert_entry_sql(conn, c, authors_added, entry, paper_identifier)
                    find_institution = False
                author_name = citation_soup["content"].split()
                last_name = author_name.pop()
                first_name = ' '.join(author_name)
                author_gender = gender.get_gender(author_name[0])
                entry += (first_name, last_name)
                find_institution = True
            elif find_institution and citation_soup["name"] == "citation_author_institution":
                institution, country = get_institution_name_and_country(citation_soup)
                entry += (institution.strip(), author_gender, country)
                print(entry)
                authors_added += 1
                entry = insert_entry_sql(conn, c, authors_added, entry, paper_identifier)
                find_institution = False


def insert_entry_sql(conn, c, authors_added, entry, paper_identifier):
    """
    Tries to insert an entry into the table authors and author_key_rank database.

    Inputs:
        conn (sqlite3 connection)
        c (sqlite3 cursor)
        authors_added (integer)
        entry (tuple with (first_name, last_name, institution, gender, country))

    Returns:
        empty tuple
    """
    try:
        c.execute('INSERT INTO authors (first_name, last_name, institution, gender, country) VALUES (?, ?, ?, ?, ?)', entry)
        conn.commit()
    except:
        print('error, author insert not unique')

    author_identifier = c.execute("select author_identifier from authors where first_name = ? and last_name = ?", (entry[0], entry[1])).fetchall()[0][0]
    rank = authors_added
    c.execute('INSERT INTO author_key_rank (author_identifier, paper_identifier,rank) VALUES (?, ?, ?)', (author_identifier, paper_identifier, rank) )
    print("author identifier", author_identifier, "paper identifier", paper_identifier)
    conn.commit()
    entry = tuple()
    return entry


def get_institution_name_and_country(citation_soup):
    """
    Obtains the first string with an institution keyword affiliated with 
    an author and the country.

    Inputs:
        citation_soup (Soup Object)
    """
    if citation_soup is not None:
        inst_strings = citation_soup["content"].lower().split(",")
        institution = ''
        country = inst_strings[-1].strip()
        for inst_string in inst_strings:
            for affiliation_word in AFFILIATIONS:
                if affiliation_word in inst_string:
                    institution = inst_string
                    return institution, country
        
        return "", country
    else:
        return "", ""


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
    soup = bs4.BeautifulSoup(html_text, 'html5lib')

    return soup





