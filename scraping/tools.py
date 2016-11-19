try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from collections import defaultdict
from scraping.password import password

import json
import requests
from ratelimit import *


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


def create_url_search(parameters, standard):
    """A function which take the parameters given for the search and
    after combining it to the standard url path for an API and returns the
    url.
    """
    url = standard
    for i in parameters:
        url += '&{}'.format(i)
    return url


@rate_limited(1)
def fetch_xml(url):
    """A function which creates the request to the API and returns the XML
    file.
    """
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise APIError(response.status_code)

    root = ET.parse(response.raw).getroot()
    return root


def xml_to_dict(branch):
    """Branch to dictionary"""
    article = defaultdict()
    for at in branch.iter():
        article.update({at.tag: at.text})

    return article


def post_to_axelbib(post):
    """A function for posting to Axelbib"""
    url = 'http://127.0.0.1:8000/article/'
    headers = {'Content-Type': 'application/json'}

    r = requests.post(url, data=json.dumps(post),
                      auth=('nikoleta', password), headers=headers)
    return r.status_code
