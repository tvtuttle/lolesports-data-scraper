# some tutorial things to test the web-scraping capabilities of requests and beautifulsoup4

# the following code is derived from:
# https://realpython.com/python-web-scraping-practical-introduction/

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# step 1: download web page using requests
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

# testing simple_get
raw_html = simple_get('https://realpython.com/blog/')
print(len(raw_html))
no_html = simple_get('https://realpython.com/blog/nope-not-gonna-find-it')
print(no_html is None)

# Part 2: Wrangling HTML with BeautifulSoup
# parses raw html strings and produces an object mirroring html structure
# this will demo the gamepedia site instead of their simple html structure
raw_html = simple_get('https://lol.gamepedia.com/LCS/2019_Season/Summer_Season/Scoreboards')
html = BeautifulSoup(raw_html, 'html.parser')
for div in html.find_all(class_='sb-p-stat'): # because class is a python keyword, use class_ instead
    print(div.text)