"""IEEE Xplore API Request.

Usage:
    IEEE/main.py -h [-au AUTHOR] [-ti TITLE] [-ab ABSTRACT] [-py YEAR] [-hc
    NUMBER]

Options:
    -h --help               show this
    -au AUTHOR              Terms to search for in Author [default: ""]
    -ti TITLE               Terms to search for in Title [default: ""]
    -ab ABSTRACT            Terms to search for in the Abstract [default: ""]
    -py YEAR                Terms to search for in Year [default: ""]
    -hc NUMBER              Number of records to fetch. [default: 25]
"""

from scraping.tools import Api
from docopt import docopt


class Ieee(Api):
    """

    """
    def __init__(self):
        self.standard = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?'

    @staticmethod
    def to_axelbib(article):
        """A function which takes a dictionary with structure of the IEEE results
        and transform it to a structure understandable by Axelbib"""
        keys = ['abstract', 'author', 'date', 'title', 'journal', 'notes', 'key']

        article['author'] = []
        for i in article['authors'].split('; '):
            article['author'].append({'name': i})
        article['date'] = {'year': int(article['py'])}
        article['journal'] = article.pop('pubtitle')
        article['notes'] = article.pop('pdf')

        first_name, last_name = article['author'][0]['name'].split(' ')
        year = article['date']['year']
        article['key'] = {'{}{}'.format(last_name, year)}

        post = {key: article[key] for key in keys}
        return post

    @staticmethod
    def parse(root):
        parents = root.getchildren()
        for _ in range(2):
            parents.remove(parents[0])
        return parents

if __name__ == '__main__':
    arguments = docopt(__doc__, version='IEEE Xplore API Request')

    parameters = ['au={}'.format(arguments['-au']), 'ti={}'.format(arguments['-ti']),
                  'ab={}'.format(arguments['-ab']), 'py={}'.format(arguments['-py']),
                  'hc={}'.format(arguments['-hc'])]

    api = Ieee()
    api.run(parameters)


