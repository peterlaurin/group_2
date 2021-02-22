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
import csv



def get_good_url(current_url, new_url, limiting_domain, url_history):
    '''
    Returns url if falls within domain of crawler.

    Input: 
    current_url, str, the current url the crawler is on
    new_url, str the new url for util.convert_if_relative_url
    limiting_domain, the domain which our crawler should stay in
    url_history, the sites the crawler has and will visit, to avoid redundancy

    Output:
    good_url, str, a url if good to visit by crawler

    '''

    good_url = new_url
    if not util.is_absolute_url(good_url):
        good_url = util.convert_if_relative_url(current_url, new_url)

    good_url = util.remove_fragment(good_url)

    if util.is_url_ok_to_follow(good_url, limiting_domain) and \
       good_url not in url_history:
        return good_url
    

def get_html(url):
    '''
    Retrieves html from a url if url is 'good' (see get_good_url)

    Input:
    url, str, a 'good' url as defined above

    Output:
    (html, visited_site), (bytes, str), the html page as a str and
    absolute site to record as history
    '''
    new_request = util.get_request(url)
    html = util.read_request(new_request)

    assert type(html) == bytes, 'bad url, html not extracted'
    visited_site = util.get_request_url(new_request)
    return html, visited_site


def process_course(course, course_map):
    '''
    Takes a course and processes the text from the title 
    and description

    Inputs: 
        course (not totally sure...tag?) the course we are processing
    
    Outputs:
        code (int): the course identifier 
        all_words (lst of strings): all the words related to that course
    '''

    title = course.find_all("p", class_ = "courseblocktitle")[0].text
    
    l = re.search(r'[A-Z]{4}',title) 
    n = re.search(r'[0-9]{5}', title)   
    if l and n: 
       string_title = l.group() + " " + n.group()

    code = course_map[string_title]

    title_words = re.findall(r'[a-zA-Z]+[a-zA-Z0-9]+', title.lower())
    desc = course.find_all("p", class_ = "courseblockdesc")[0].text
    desc_words = re.findall(r'[a-zA-Z]+[a-zA-Z0-9]+', desc.lower())

    all_words = title_words + desc_words 

    return code, all_words   

def add_words(code, word_list, word_dict):
    '''
    Takes a list of words and a course and adds the course code to the word 
    in the dictionary

    Inputs:
        a string from the course title and description
        a code for the course 
    Outputs:
        none

    '''
    for word in word_list:
        if word in INDEX_IGNORE:
            continue
            
        if word not in word_dict:
            word_dict[word] = []
        if code not in word_dict[word]:
            word_dict[word].append(code)        



def go(num_pages_to_crawl, course_map_filename, index_filename):
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

    

    search_url = ("https://www.nature.com/search?article_type=protocols, \
                   research,reviews&subject=")
    search_url = ('https://www.nature.com/search?article_type=protocols%2Cresearch%2Creviews&subject=')
    suffix = '&page='
    
    limiting_domain = "https://www.nature.com"

    search_urls = []

    num_articles_per_field = 10

    num_pages_to_visit = int(np.ceil(num_articles_per_field / 50))

    fields = ['biological-sciences', 'business-and-commerce', 
              'earth-and-environmental-sciences','health-sciences',
              'humanities', 'physical-sciences', 
              'scientific-community-and-society','social-science']

    for field in fields:
        for i in range(num_pages_to_visit):
            new_url = search_url + field + suffix + str(i + 1)
            search_urls.append(new_url)


    
    

    link_queue = queue.Queue()
    url_history = set()
     
    num_pages_to_visit = int(np.ceil(num_articles_per_field / 50))

    #setup search for each field 
    #link_queue.put(search_url, fields)

    new_request = util.get_request(url)
    html = util.read_request(new_request)
    soup = bs4.BeautifulSoup(html, features = 'html.parser')
    article_links = search_soup.find_all('h2', class_ = 'h3 extra-tight-line-height', itemprop = 'headline')

    num_articles_extracted = 0

    while num_articles_extracted < num_articles_per_field:
        
        
        html, visited_site = get_html(current_url)
        
        #add links to queue
        
        for entry in article_links:
            part_link = entry.a['href']
            article_link = util.convert_if_relative_url()
            
            
            if link.has_attr('href'):
                potential_link = link['href']
                good_url = get_good_url(current_url, potential_link, 
                                        limiting_domain, url_history)
                if good_url and len(url_history) < num_pages_to_crawl:
                    link_queue.put(good_url)
                    url_history.append(good_url)

        #add course info to word dict
        process_soup(soup, word_dict, course_map)

    #write csv
    write_csv(index_filename, word_dict)







if __name__ == "__main__":
    usage = "python3 crawl.py <number of pages to crawl>"
    args_len = len(sys.argv)
    course_map_filename = "course_map.json"
    index_filename = "catalog_index.csv"
    if args_len == 1:
        num_pages_to_crawl = 1000
    elif args_len == 2:
        try:
            num_pages_to_crawl = int(sys.argv[1])
        except ValueError:
            print(usage)
            sys.exit(0)
    else:
        print(usage)
        sys.exit(0)

    go(num_pages_to_crawl, course_map_filename, index_filename)
