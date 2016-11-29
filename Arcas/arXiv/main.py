from Arcas.tools import Api
from xml.etree import ElementTree
import hashlib


class Arxiv(Api):
    """
     API argument is 'ieee'.
    """
    def __init__(self):
        self.standard = 'http://export.arxiv.org/api/query?search_query='

    @staticmethod
    def to_json(article):
        """A function which takes a dictionary with structure of the arXiv
        results and transform it to a standardized format.
        """
        keys = ['key', 'unique_key', 'title', 'abstract', 'author', 'date',
                'journal', 'pages', 'labels', 'read', 'key_word', 'provelance',
                'list_strategies']

        old_keys = list(article.keys())
        for i in old_keys:
            keep = i.split('}')
            article[keep[-1]] = article.pop(i)

        article['author'] = []
        for i in article['name'].split(','):
            article['author'].append({'name': i})

        article['date'] = {'year': int(article['published'].split('-')[0])}
        try:
            article['journal'] = article.pop('journal_ref')
        except:
            article['journal'] = "arXiv"
        article['key_word'] = []
        if article['primary_category'] is not None:
            for i in article['primary_category']:
                article['key_word'].append({'key_work': i})
        article['abstract'] = article.pop('summary')
        article['labels'], article['list_strategies'] = [], []
        article['pages'] = ""
        article['provelance'] = 'arXiv'
        article['read'] = False

        year = article['date']['year']
        full_name = article['author'][0]['name'].split(' ')
        article['key'] = '{}{}'.format(full_name[-1], year)

        string = '{}{}{}{}'.format(full_name[-1], article['title'], year,
                                   article['abstract'])
        hash_object = hashlib.md5(string.encode('utf-8'))
        article['unique_key'] = hash_object.hexdigest()

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
