try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from collections import defaultdict
from .password import password

import json
import requests
from ratelimit import *


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


class Api():
    """A class ..."""
    def __init__(self):
        self.standard = None

    def create_url_search(self, parameters):
        """A function which take the parameters given for the search and
        after combining it to the standard url path for an API and returns the
        url.
        """
        url = self.standard
        for i in parameters:
            url += '&{}'.format(i)
        return url

    @staticmethod
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

    @staticmethod
    def xml_to_dict(branch):
        """Branch to dictionary"""
        article = defaultdict()
        for at in branch.iter():
            article.update({at.tag: at.text})

        return article

    @staticmethod
    def post_to_axelbib(post):
        """A function for posting to Axelbib"""
        url = 'http://127.0.0.1:8000/article/'
        headers = {'Content-Type': 'application/json'}

        r = requests.post(url, data=json.dumps(post),
                          auth=('nikoleta', password), headers=headers)
        return r.status_code


    @staticmethod
    def to_axelbib(article):
        pass

    @staticmethod
    def parse(root):
        pass

    def run(self, parameters, filename="status_report"):
        """
        Runing...
        """
        url = self.create_url_search(parameters=parameters)
        root = self.fetch_xml(url)
        parents = self.parse(root)

        for document in parents:
            article = self.xml_to_dict(document)
            post = self.to_axelbib(article)
            send = self.post_to_axelbib(post)

            with open(filename, 'a') as textfile:
                textfile.write('{}{}\n'.format(post['key'], send))
