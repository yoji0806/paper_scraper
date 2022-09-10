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

    dic_issue_link_title = {}
    
    soup_obj = soup(url_aer_issues)
    lst_issues = soup_obj.find_all('a', href=re.compile('/issues/'))

    for issue in lst_issues:
        link = base_url + issue['href']
        title = issue.text

        dic_issue_link_title[link] = title
        
        
    return dic_issue_link_title



def scrape_aer_papers_in_issue(url_aer_issue):
    """ get paper titles and links of a issue.
    
    Args:
        url_aer_issue (str): link of a issue page.(ex: "https://www.aeaweb.org/issues/689")
    
    Returns:
        dic_paper_link_title (dict): key is paper link, value is paper title.
    """
    
    dic_paper_link_title = {}
    
    soup_obj = soup(url_aer_issue)
    lst_papers = soup_obj.find_all('a', href=re.compile('/articles?'))
    
    for paper in lst_papers:
        link = base_url_aer + paper['href']
        title = paper.text

        if title=="Front Matter":
            continue

        dic_paper_link_title[link] = title
        
    return dic_paper_link_title



def scrape_aer_info_in_paper(url_aer_paper):
    """get information about a paper.
    
    returns paper information something like below.
    
        {
            "title_str": "Aggregating Distributional Treatment Effects: A Bayesian Hierarchical Analysis of the Microcredit Literature",
            "author_lst": [
                {
                    "name": "Meager, Rachael",
                    "institution": "London School of Economics and Political Science"
                }
            ],
            "abstract_str": "(June 2022) - Expanding credit access in developing contexts could help some households while harming others. Microcredit studies show different effects at different quantiles of household profit, including some negative effects; yet these findings also differ across studies. I develop new Bayesian hierarchical models to aggregate the evidence on these distributional effects for mixture-type outcomes such as household profit. Applying them to microcredit, I find a precise zero effect from the fifth to seventy-fifth quantiles, and uncertain yet large effects on the upper tails, particularly for households with business experience. These quantile estimates are more reliable than averages because the data are fat tailed.",
            "categorycode_lst": [
                "G21",
                "G51",
                "L25",
                "O16",
                "P34"
            ]
        }
    
    
    Args:
        url_aer_paper (str): link of a paper page.(ex: "https://www.aeaweb.org/articles?id=10.1257/aer.20181811")
    
    Returns:
        paper_info (dict): paper information
    """
    
    soup_obj = soup(url_aer_paper)
    lst_metadata = soup_obj.find_all('meta')

    paper_info = {}
    lst_dict_author = []
    str_title = ''
    str_abstract = ''

    #TODO: get "Additional Material"information.
    lst_additional_materials = []
    
    #TODO: get category text information.
    lst_dict_category = []
    
    lst_jel_categorycode = []


    dict_author = {
            'name': '',
            'institution': ''
        }

    for metadata in lst_metadata:
        name_metadata = metadata.get('name')

        if(name_metadata == 'citation_author'):    
            author_name = metadata.get('content')
            dict_author['name'] = author_name
            continue


        if(name_metadata == 'citation_author_institution'):
            author_institution = metadata.get('content')
            dict_author['institution'] = author_institution

            copy_dict_author = dict_author.copy()        
            lst_dict_author.append(copy_dict_author)
            continue
    
    
        if(name_metadata == 'citation_title'):
            str_title = metadata.get('content')
            continue
    

        if(name_metadata == 'twitter:description'):
            str_abstract = metadata.get('content')
            continue

    # get category codes
    soup_class_code = soup_obj.find_all("strong", {"class":"code"})

    for item in soup_class_code:
        category_code = item.contents[0]
        lst_jel_categorycode.append(category_code)

    
    paper_info["title_str"] = str_title
    paper_info["author_lst"] = lst_dict_author
    paper_info["abstract_str"] = str_abstract
    paper_info["categorycode_lst"] = lst_jel_categorycode
    
    #TODO
    #paper_info["category"] = xxx
    #paper_info["additional_material"] = xxx
    
    
    return paper_info