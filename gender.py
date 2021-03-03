import bs4 
import urllib.request
import util
from urllib.request import Request, urlopen
import re
import util
import bs4
import queue
import json
import sys
import csv
import math
import sqlite3


def get_gender(name):

    url = "https://www.names.org/n/" + name + "/about"
    
    try:
        req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        html_text = urlopen(req).read()
    except:
        return "name not found"

    soup = bs4.BeautifulSoup(html_text, 'html.parser')

    gender_girl = soup.find_all("div", class_ = "name-box gender-girl container page-section")
    if len(gender_girl) != 0:
        return "girl"
    
    gender_boy = soup.find_all("div", class_ = "name-box gender-boy container page-section")
    if len(gender_boy) != 0:
        return "boy"
    
    gender_neutral = soup.find_all("div", class_ = "name-box gender-neutral container page-section")
    if len(gender_neutral) != 0: 
        return "gender neutral"


