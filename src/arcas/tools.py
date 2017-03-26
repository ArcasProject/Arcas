from xml.etree import ElementTree

import requests
import hashlib
import itertools
import pandas as pd
from ratelimit import *


class APIError(Exception):
    """An API Error Exception."""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


class Api():

    def __init__(self, standard):
        """Initializations"""
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
    def xml_to_dict(record):
        """Xml response with information on article to dictionary"""
        d = {}
        for at in record.iter():
            if at.tag in d and at.text is not None:
                d[at.tag] += ',{}'.format(at.text)
            else:
                d.update({at.tag: at.text})
        return d

    @staticmethod
    def keys():
        pass

    @staticmethod
    def to_dataframe(raw_article):
        pass

    @staticmethod
    def parse(root):
        pass

    @staticmethod
    def parameters_fix(author=None, title=None, abstract=None, year=None,
                       records=None, start=None):
        pass

    @staticmethod
    def get_root(response):
        root = ElementTree.parse(response.raw).getroot()
        return root

    @staticmethod
    def lower_case(post):
        post = dict((k.lower() if isinstance(k, str) else k,
                     v.lower() if isinstance(v, str) else v) for k, v in
                    post.items())
        return post

    @staticmethod
    def create_keys(raw_article):
        """
        Returns public key 'AuthorYear' and
        unique key hash('Author''Title''Year''Abstract')
        """
        try:
            full_name = raw_article['author'][0].split(' ')
        except TypeError:
            full_name = [None]
        year = raw_article['date']
        string = '{}{}{}{}'.format(full_name[-1], raw_article['title'], year,
                                   raw_article['abstract'])

        hash_object = hashlib.md5(string.encode('utf-8'))

        key = '{}{}'.format(full_name[-1], year)
        unique_key = hash_object.hexdigest()

        return key, unique_key

    def dict_to_dataframe(self, raw_article):
        """
        Takes a dictionary and returns a dataframe
        """
        values = []
        for key in self.keys():
            if type(raw_article[key]) is not list:
                values.append([raw_article[key]])
            else:
                values.append(raw_article[key])
        data = []
        for row in itertools.product(*values):
            data.append(row)
        df = pd.DataFrame(data, columns=self.keys())
        return df

    def validate_post(self, arguments, df):
        """
        Checks if the query arguments abstract and title  were satisfied.

        Parameters:
            - arguments
            - post
        Returns:
           - True of False
        """
        arguments = self.lower_case(arguments)
        word = [arguments['-b'], arguments['-t']]

        fields = ['abstract', 'title']
        check = [list(df[f].unique()) for f in fields]
        val = []
        for i, w in enumerate(word):
            if w is not None:
                for j in w.split(' '):
                    if check[i][0] is not None:
                        val.append(j in check[i][0].lower())
        return all(val)

    @staticmethod
    def export(df, filename):
        """ Write the results to a json file
        """
        df.to_json(filename)

    def run(self, url, arguments, validate):
        """Putting everything together. Makes the request,
        transforms from xml to dict to a standardized format and output to
        json file.
        """
        response = self.make_request(url)
        root = self.get_root(response)
        raw_articles = self.parse(root)
        if not raw_articles:
            raise ValueError('Empty results at {}'.format(url))
        else:
            dfs = []
            for raw_article in raw_articles:
                df = self.to_dataframe(raw_article)

                if validate is True:
                    try:
                        self.validate_post(arguments, df)
                    except:
                        string = "Validation for article '{}', with " \
                                 "citation  key:{}.".format(
                                  df['title'], df['key'])
                        raise NotImplementedError(string)

                dfs.append(df)
            df = pd.concat(dfs, ignore_index=True)

            self.export(df, filename=arguments['-f'])




