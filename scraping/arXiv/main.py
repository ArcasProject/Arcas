from scraping.tools import Api
from xml.etree import ElementTree


class Arxiv(Api):
    """
     API argument is 'ieee'.
    """
    def __init__(self):
        self.standard = 'http://export.arxiv.org/api/query?search_query='

    @staticmethod
    def to_axelbib(article):
        """A function which takes a dictionary with structure of the IEEE results
        and transform it to a structure understandable by Axelbib"""
        keys = ['key', 'title', 'abstract', 'author', 'date', 'journal',
                'pages', 'labels', 'list_strategies']

        old_keys = list(article.keys())
        for i in range(len(old_keys)):
            dis, keep = old_keys[i].split('}')
            article[keep] = article.pop(old_keys[i])

        article['author'] = []
        for i in article['name'].split(','):
            article['author'].append({'name': i})

        article['date'] = {'year': int(article['published'].split('-')[0])}
        try:
            article['journal'] = article.pop('journal_ref')
        except:
            article['journal'] = ""
        year = article['date']['year']
        full_name = article['author'][0]['name'].split(' ')
        article['key'] = '{}{}'.format(full_name[-1], year)
        article['pages'] = ""
        article['abstract'] = article.pop('summary')
        article['labels'], article['list_strategies'] = [], []

        post = {key: article[key] for key in keys}

        return post

    @staticmethod
    def parse(root):
        """Removing unwanted branches."""
        parents = root.getchildren()
        for _ in range(7):
            parents.remove(parents[0])
        return parents

    @staticmethod
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('au:{}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('ti:{}'.format(arguments['-t']))
        if arguments['-b'] is not None:
            parameters.append('ab:{}'.format(arguments['-b']))
        if arguments['-r'] is not None:
            parameters.append('max_results={}'.format(arguments['-r']))
        if arguments['-s'] is not None:
            parameters.append('start={}'.format(arguments['-s']))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root
