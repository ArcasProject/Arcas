from xml.etree import ElementTree
from collections import defaultdict

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
        url += parameters[0]
        for i in parameters[1:]:
            url += '&{}'.format(i)
        return url

    @staticmethod
    @rate_limited(3)
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
    def to_json(article):
        pass

    @staticmethod
    def parse(root):
        pass

    @staticmethod
    def parameters_fix(arguments):
        pass

    @staticmethod
    def get_root(response):
        root = ElementTree.parse(response.raw).getroot()
        return root

    def run(self, parameters, filename="status_report"):
        """Putting everything together. Creates the url, makes the request,
        transforms from xml to dict to a standardized format and output to
        json file.
        """

        url = self.create_url_search(parameters=parameters)
        response = self.make_request(url)
        root = self.get_root(response)

        try:
            parents = self.parse(root)
            for document in parents:
                article = self.xml_to_dict(document)
                post = self.to_json(article)

                with open('result.json', 'w') as jsonfile:
                   json.dump(post, jsonfile)

                with open(filename, 'a') as textfile:
                   textfile.write('{}--{}--{}--({})\n'.format(post['key'],
                                                              post['title'],
                                                              url,
                                                            post['unique_key']))
        except:
            raise ValueError('Empty Results.(url:{})'.format(url))





