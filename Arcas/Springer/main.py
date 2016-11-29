from Arcas.tools import Api
import hashlib


class Springer(Api):
    """
     API argument is 'springer'.
    """
    def __init__(self):
        self.standard = 'http://api.springer.com/metadata/pam?q='
        self.key_api = 'b64bdd033bc495c894914f34a8690785'

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:]:
            url += '&{}'.format(i)
        url += '&api_key={}'.format(self.key_api)
        return url

    @staticmethod
    def to_json(article):
        """A function which takes a dictionary with structure of the Springer
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
        for i in article['creator'].split(','):
            article['author'].append({'name': i})

        article['date'] = {
            'year': int(article['publicationDate'].split('-')[0])}
        article['journal'] = article.pop('publicationName')
        article['key_word'] = []
        article['abstract'] = article.pop('p')
        article['labels'], article['list_strategies'] = [], []
        article['pages'] = ""
        article['provelance'] = 'Springer'
        article['read'] = False

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
        parents = root.getchildren()[3]
        return parents

    @staticmethod
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('name:{}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('title:{}'.format(arguments['-t']))
        if arguments['-b'] is not None:
            parameters.append('keyword:{}'.format(arguments['-b']))
        if arguments['-y'] is not None:
            parameters.append('date:{}'.format(arguments['-y']))
        if arguments['-r'] is not None:
            parameters.append('s={}'.format(arguments['-r']))
        if arguments['-s'] is not None:
            parameters.append('p=1'.format(arguments['-s']))

        return parameters



