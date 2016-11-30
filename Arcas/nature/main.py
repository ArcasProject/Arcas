from Arcas.tools import Api


class Nature(Api):
    """
    API argument is 'nature'.
    """
    def __init__(self):
        self.standard = 'http://www.nature.com/opensearch/request?queryType=cql&query='

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:-2]:
            url += '+AND+{}'.format(i)
        for j in parameters[-2:]:
            url += '&{}'.format(j)
        return url

    @staticmethod
    def parse(root):
        """Removing unwanted branches."""
        parents = root.getchildren()[2]

        if not parents:
            articles = False
        else:
            temp = {}
            articles = []
            for count, i in enumerate(parents.iter()):
                if (count + 1) % 26 == 0:
                    articles.append(temp)
                    temp = {}
                else:
                    temp.update({i.tag: i.text})
        return articles

    def to_json(self, article):
        """A function which takes a dictionary with structure of the nature
        results and transform it to a standardized format.
        """
        old_keys = list(article.keys())
        for i in old_keys:
            keep = i.split('}')
            article[keep[-1]] = article.pop(i)

        article['author'] = []
        for i in article['creator'].split(',  '):
            article['author'].append({'name': i})
        article['key_word'] = []

        article['abstract'] = article['description']
        article['date'] = {
            'year': int(article['publicationDate'].split('-')[0])}
        article['journal'] = article.pop('publicationName')
        article['pages'] = ""
        article['provenance'] = 'Nature'
        article['read'] = False
        article['labels'], article['list_strategies'] = [], []

        article['key'], article['unique_key'] = self.create_keys(article)

        post = {key: article[key] for key in self.keys()}

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
            parameters.append('maximumRecords={}'.format(arguments['-r']))
        if arguments['-s'] is not None:
            parameters.append('startRecord={}'.format(arguments['-s']))

        return parameters
