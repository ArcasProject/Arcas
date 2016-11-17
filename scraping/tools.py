try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from collections import defaultdict
from password import password

import json
import requests

# standard = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?'


# 1st function: Create the URL
def create_url_search(parameters, standard):
    """A function which take the parameters given for the search and
    after combining it to the standard url path for IEEE explorer returns the
    url.
    """
    url = '{}&{}'.format(standard, [_ for _ in parameters])
    return url


# 2nd function: Get the request
def fetch_xml(url):
    """A function which creates the request to the API and returns the XML
    file.
    """
    response = requests.get(url, stream=True)
    # response.status_code check error
    root = ET.parse(response.raw).getroot()
    return root


# 3rd function: Xml to dict
def xml_to_dict(branch):
    """Branch to dictionary"""
    article = defaultdict()
    for at in branch.iter():
        article.update({at.tag: at.text})

    return article


# 4th Transformation to what suites Axelbib
def iee_to_axelbib(article):
    """A function which takes a dictionary with structure of the IEEE results
    and transform it to a structure understandable by Axelbib"""
    keys = ['abstract', 'author', 'date', 'title', 'journal', 'notes', 'key']

    article['author'] = []
    for i in article['authors'].split(';'):
        article['author'].append({'name': i})
    article['date'] = {'year': int(article['py'])}
    article['journal'] = article.pop('pubtitle')
    article['notes'] = article.pop('pdf')

    first_name, last_name = article['author'][0]['name'].split('. ')
    year = article['date']['year']
    article['key'] = {'key': '{}{}'.format(last_name, year)}

    post = {key: article[key] for key in keys}
    return post


# 5th function: Post to Axelbib
def post_to_axelbib(post):
    """A function for posting to Axelbib"""
    url = 'http://127.0.0.1:8000/article/'
    headers = {'Content-Type': 'application/json'}

    r = requests.post(url, data=json.dumps(post),
                      auth=('nikoleta', password), headers=headers)
    return r.status_code