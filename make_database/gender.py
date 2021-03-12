import bs4 
import util
from urllib.request import Request, urlopen
import unidecode



def get_gender(name):
    '''
    Assigns gender from first_name using names.org (multiyear census data)

    Input:
        name, str, the first_name (stripped) of the author

    Output:
        gender, str, a gender assignment or additional category

    '''

    unaccented_name = unidecode.unidecode(name)

    url = "https://www.names.org/n/" + unaccented_name + "/about"
    
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
    
    return 'unknown'


