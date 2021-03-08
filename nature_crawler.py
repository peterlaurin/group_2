# CS122: group_2 project
#
#  Author: Peter Laurin
#

import re
import util
import bs4
import queue
import json
import sys
import sqlite3
import numpy as np
import gender


AFFILIATIONS = ['university', 'université', 'universität', 'ucla', 'universidad'
, 'univ', 'università', 'institute', 'college', 'laboratory']

def get_paper_links(number_of_articles, fields):
    '''
    Crawls through Nature search pages, and pulls article links 
    from different fields

    Input:
    number of articles, int number of articles to find 
    fields, list of field str, all major fields in nature.com/subjects
    
    Output:
    paper_links, list of paper urls (str)
    '''
    search_urls = []
    paper_links = []

    num_articles_per_field = number_of_articles // 8 
    num_pages_to_visit = int(np.ceil(num_articles_per_field / 50))
    num_on_last_page = num_articles_per_field % 50

    for field in fields:
        for i in range(num_pages_to_visit):
            new_url = search_url + field + suffix + str(i + 1)
            search_urls.append(new_url)
        
    for url in search_urls:
        num_to_search = 50
        if int(url[-1]) == num_pages_to_visit:
            num_to_search = num_on_last_page

        new_request = util.get_request(url)
        html = util.read_request(new_request)
        search_soup = bs4.BeautifulSoup(html, features = 'html.parser')
        article_links = search_soup.find_all('h2', 
                        class_ = 'h3 extra-tight-line-height', 
                        itemprop = 'headline')
        article_links = article_links[:num_to_search]
        paper_links.extend([i.find('a')['href'] for i in article_links])
    
    return paper_links

def get_institution_name(author, authors):
    '''
    Extracts name of institution (and country of institution)
    from author info, if present in a group of word AFFLIATES

    Input:
    author, Beautiful Soup tag, of author info
    authors, list of Beautiful Soup tags, of all authors

    Output:
    institution, str of institution if AFFILIATE word matched
    country, str of country of institution
    '''
    pot_institution = author.nextSibling
    ins_string = ''
    endpt = "https://www.nature.com/platform/readcube-access"
    while (pot_institution not in authors) and (ins_string != endpt):
        if pot_institution == '\n':
            pot_institution = pot_institution.nextSibling
            continue
        ins_string = pot_institution['content']
        print(ins_string)
        for word in AFFILIATIONS:
            if word in ins_string.lower():
                ins_list = ins_string.lower().split(',')
                country = ins_list[-1].strip()
                institution = ins_list[-3].strip()
                return institution, country
        pot_institution = pot_institution.nextSibling
    return '', ''

def nature_crawler(number_of_articles):
    '''
    Crawl the college catalog and generate a CSV file with an index.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        course_map_filename: the name of a JSON file that contains the mapping of
          course codes to course identifiers
        index_filename: the name for the CSV of the index.

    Outputs:
        CSV file of the index
    '''

    conn = sqlite3.connect('journals.db')
    c = conn.cursor()

    search_url = ('https://www.nature.com/search?article_type=protocols\
                  %2Cresearch%2Creviews&subject=')
    suffix = '&page='
    
    home_domain = "https://www.nature.com"

    search_urls = []

    fields = ['biological-sciences', 'business-and-commerce', 
              'earth-and-environmental-sciences','health-sciences',
              'humanities', 'physical-sciences', 
              'scientific-community-and-society','social-science']

    paper_links = get_paper_links(number_of_articles, fields)


    for i, link in enumerate(paper_links):
        new_request = util.get_request(home_domain + link)
        html = util.read_request(new_request)
        article_soup = bs4.BeautifulSoup(html, features = 'html.parser')
        authors = article_soup.find_all('meta', {'name':'citation_author'})

        #process paper

        full_title = article_soup.find('title').text.split(' | ')
        paper_title = full_title[0]
        print(paper_title)
        journal = full_title[1]
        num_authors = len(authors)
        year_find = article_soup.find('meta', {'name':'dc.date'})['content']
        year = year_find.split('-')[0]
        num_articles_per_field = number_of_articles // 8
        field_index = int(np.ceil(i // num_articles_per_field))
        field = fields[field_index]
        insert = (paper_title, year, journal, field, num_authors)

        try:
            c.execute('INSERT INTO papers(title, year, journal, field, \
                       num_authors) VALUES (?, ?, ?, ?, ?)', insert)
            conn.commit()
            
        except: 
            print('error, insert not unique')
            continue

        fetch = c.execute('SELECT paper_identifier FROM papers WHERE \
                           title = ?', (paper_title,))
        paper_identifier = fetch.fetchone()[0]

        #process author

        for rank, author in enumerate(authors): 
            try:
                name = author['content'].split()
                last_name = name.pop()
                first_name = ' '.join(name)
                gen = gender.get_gender(name[0].strip())
                institution, country = get_institution_name(author, authors)
                insert = (first_name, last_name, institution, gen, country)
            except:
                print('unable to extract')
                continue
            try:
                c.execute('INSERT INTO authors(first_name, last_name, \
                           institution, gender, country) VALUES (?, ?, ?, \
                           ?, ?)', insert)
                conn.commit()
            except:
                print('author already here')
            
            fetch = c.execute('SELECT author_identifier FROM authors WHERE \
                               first_name = ? AND last_name = ?', (first_name,\
                               last_name))
            author_identifier = fetch.fetchone()[0]
            insert = (author_identifier, paper_identifier, rank + 1)
                
            c.execute('INSERT INTO author_key_rank(author_identifier, \
                       paper_identifier, rank) VALUES (?, ?, ?)', insert)
            conn.commit()
                
        print(i)



if __name__ == "__main__":
    usage = "python3 nature_crawler.py <number of pages to crawl>"
    args_len = len(sys.argv)
    if args_len == 1:
        number_of_articles = 1500
    elif args_len == 2:
        try:
            number_of_articles = int(sys.argv[1])
        except ValueError:
            print(usage)
            sys.exit(0)
    else:
        print(usage)
        sys.exit(0)

    nature_crawler(number_of_articles)
