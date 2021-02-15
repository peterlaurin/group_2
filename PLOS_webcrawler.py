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
    Crawl the PLOS One and generate a dictionary.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl

    Outputs:
        dictionary mapping author identifiers to list of variables
    '''

    starting_url = ("https://journals.plos.org/plosone/browse#")
    limiting_domain = "journals.plos.org"

    url_queue = queue.Queue()
    urls_visited = []
    index = {}
    
    request = util.get_request(starting_url)

    for i in range(num_pages_to_crawl):
        if request:
            html_text = util.read_request(request)
            current_url = util.get_request_url(request) 
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