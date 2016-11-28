from Arcas.tools import Api
import hashlib


class Ieee(Api):
    """
     API argument is 'ieee'.
    """
    def __init__(self):
        self.standard = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?'

    @staticmethod
    def to_json(article):
        """A function which takes a dictionary with structure of the IEEE
        results and transform it to a standardized format.
        """
        keys = ['key', 'unique_key', 'title', 'abstract', 'author', 'date',
                'journal', 'pages', 'labels', 'read', 'key_word', 'provelance',
                'list_strategies']

        article['author'] = []
        for i in article['authors'].split(';  '):
            article['author'].append({'name': i})
        article['key_word'] = []
        for j in article['term'].split(','):
            article['key_word'].append({'key_work': j})

        article['date'] = {'year': int(article['py'])}
        article['journal'] = article.pop('pubtitle')
        article['pages'] = '{}-{}'.format(article['spage'], article['epage'])
        article['provelance'] = 'IEEE'
        article['read'] = False
        article['labels'], article['list_strategies'] = [], []

        full_name = article['author'][0]['name'].split(' ')
        year = article['date']['year']
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
        for _ in range(2):
            parents.remove(parents[0])
        return parents

    @staticmethod
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('au={}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('ti={}'.format(arguments['-t']))
        if arguments['-b'] is not None:
            parameters.append('ab={}'.format(arguments['-b']))
        if arguments['-y'] is not None:
            parameters.append('py={}'.format(arguments['-y']))
        if arguments['-r'] is not None:
            parameters.append('hc={}'.format(arguments['-r']))
        if arguments['-s'] is not None:
            parameters.append('rs={}'.format(arguments['-s']))

        return parameters



