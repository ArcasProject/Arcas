from xml.etree import ElementTree
from collections import defaultdict
from .password import password

import json
import requests
from ratelimit import *


class APIError(Exception):
    """An API Error Exception."""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


class Api():

    def __init__(self, standard):
        """Initialize standard url. Each API has a different standardised url
        path before the extra arguments."""
        self.standard = standard

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        for i in parameters:
            url += '&{}'.format(i)
        return url

    @staticmethod
    @rate_limited(1)
    def make_request(url):
        """Request from an API and returns response."""
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise APIError(response.status_code)
        return response

    @staticmethod
    def xml_to_dict(branch):
        """Branch to dictionary"""
        article = defaultdict()
        for at in branch.iter():
            if at.tag in article and at.text != None:
                article[at.tag] += ',{}'.format(at.text)
            else:
                article.update({at.tag: at.text})
        return article

    @staticmethod
    def post_to_axelbib(post):
        """Posting dict to Axelbib"""
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

    @staticmethod
    def parameters_fix(arguments):
        pass

    def run(self, parameters, filename="status_report"):
        """Putting everything together. Creates the url, makes the request,
        transforms from xml to dict to axelbib format and posts it."""

        url = self.create_url_search(parameters=parameters)
        response = self.make_request(url)
        root = ElementTree.parse(response.raw).getroot()
        parents = self.parse(root)

        for document in parents:
            article = self.xml_to_dict(document)
            post = self.to_axelbib(article)
            send = self.post_to_axelbib(post)

            with open(filename, 'a') as textfile:
                textfile.write('{} -- {}\n'.format(post['key'], send))
