from Arcas.tools import Api
import hashlib


class Nature(Api):
    """q
     API argument is 'nature'.
    """
    def __init__(self):
        self.standard= 'http://www.nature.com/opensearch/request?'

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:]:
            url += '+AND+{}'.format(i)
        return url

    @staticmethod
    def parse(root):
        """Removing unwanted branches."""
        parents = root.getchildren()[2]
        return parents

    @staticmethod
    def to_json(article):
        """A function which takes a dictionary with structure of the nature
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
        for i in article['creator'].split(',  '):
            article['author'].append({'name': i})
        article['key_word'] = []
        for j in article['subject'].split(','):
            article['key_word'].append({'key_work': j})

        article['abstract'] = article['description']
        article['date'] = {
            'year': int(article['publicationDate'].split('-')[0])}
        article['journal'] = article.pop('publicationName')
        article['pages'] = ""
        article['provelance'] = 'Nature'
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
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('dc.creator={}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('dc.title adj {}'.format(arguments['-t']))
        if arguments['-b'] is not None:
            parameters.append('dc.description adj {}'.format(arguments['-b']))
        if arguments['-y'] is not None:
            parameters.append('prism.publicationDate={}'.format(arguments['-y']))
        if arguments['-r'] is not None:
            parameters.append('maximumRecords=1')
        if arguments['-s'] is not None:
            parameters.append('startRecord={}'.format(arguments['-s']))

        return parameters
