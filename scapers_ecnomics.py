from bs4 import BeautifulSoup

import requests
import re



base_url_aer = "https://www.aeaweb.org"
url_aer_issues = base_url_aer + "/journals/aer/issues"


def soup(url, parser="html.parser"):
    """Get a web page and parse
    
    Args:
        url (string): url of a web page.
        parser (string): parser available in bs4.

    Returns:
        soup_obj (bs4.BeautifulSoup): soup oject
    """
    
    response = requests.get(url)

    #to avoid character corruption
    response.encoding = response.apparent_encoding
    soup_obj = BeautifulSoup(response.text, parser)
    
    return soup_obj


def scrape_aer_issues():
    """get issue titles and links
    
    Get issues from AER web page.
    Older issues is stored in JSTOR.
    
    Args:
    
    Returns:
        dic_link_title (dict): key is issue link, value is issue title.
    """
    
    base_url = "https://www.aeaweb.org"
    url = base_url + "/journals/aer/issues"
    dic_link_title = {}
    
    soup_obj = soup(url)
    lst_issues = soup_obj.find_all('a', href=re.compile('/issues/'))

    for issue in lst_issues:
        link = base_url + issue['href']
        title = issue.text

        dic_title_link[link] = title
        
        
    return dic_link_title