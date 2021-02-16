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

def go(num_pages_to_crawl):
    '''
    Crawl the PLOS One and generate a database. Automatically samples even
    number of articles from each subject area based on num_pages_to_crawl.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl

    Outputs:
        dictionary mapping author identifiers to list of variables
    '''
    urls_visited = []
    starting_url = ("https://journals.plos.org/plosone/browse")
    limiting_domain = "journals.plos.org"
    request = util.get_request(starting_url) 

    #get list of urls for subject areas
    html_text = util.read_request(request)
    current_url = util.get_request_url(request)  #gets correct url in case of redirection
    soup = bs4.BeautifulSoup(html_text, 'html5lib')
    soup_dropdown_menu_lst = soup.find_all("ul", typeof="v:Breadcrumb")
    soup_subject_urls_lst = soup_dropdown_menu_lst[0].find_all("a")
    subject_urls_lst = []
    for a_tag in soup_subject_urls_lst[1:]:
        url = util.convert_if_relative_url(current_url, a_tag["href"])
        subject_urls_lst.append(url)

    #iterate through subject areas
    #for loop counting max urls per subject to crawl
    #get all urls from page function => add to queue
    #iterate through queue
    #when queue empty get next page function
    #decide urls to crawl per subject: num_pages_to_crawl/11.lower()
    #








    url_queue = queue.Queue()
    urls_visited = []
    index = {}
    
    request = util.get_request(starting_url) 

    for i in range(num_pages_to_crawl):
        if request:
            html_text = util.read_request(request)
            current_url = util.get_request_url(request)  #gets correct url in case of redirection
            urls_visited.append(current_url)
            process_webpage(html_text, index, course_map)
            urls = get_relevant_urls(html_text, current_url, limiting_domain)
            for url in urls:
                url_queue.put(url)
            
        if url_queue.empty():
            generate_csv(index, index_filename)
            return 
        next_url = url_queue.get()
        while next_url in urls_visited:
            if url_queue.empty():
                generate_csv(index, index_filename)
                return 
            next_url = url_queue.get()
        request = util.get_request(next_url)
    
    generate_csv(index, index_filename)
    return 