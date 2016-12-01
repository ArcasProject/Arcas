from arcas.tools import Api


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

    def to_json(self, article):
        """A function which takes a dictionary with structure of the Springer
        results and transform it to a standardized format.
        """
        old_keys = list(article.keys())
        for i in old_keys:
            keep = i.split('}')
            article[keep[-1]] = article.pop(i)

        article['author'] = []
        for i in article['creator'].split(','):
            article['author'].append({'name': i})
        try:
            article['date'] = {
                'year': int(article['publicationDate'].split('-')[0])}
            article['abstract'] = article.pop('p')
        except:
            article['date'] = {'year': 0}
            article['abstract'] = ""
        article['journal'] = article.pop('publicationName')
        article['key_word'] = []
        article['labels'], article['list_strategies'] = [], []
        article['pages'] = ""
        article['provenance'] = 'Springer'
        article['read'] = False

        article['key'], article['unique_key'] = self.create_keys(article)

        post = {key: article[key] for key in self.keys()}

        return post

    @staticmethod
    def parse(root):
        """Removing unwanted branches."""
        parents = root.getchildren()[3]
        if not parents:
            articles = False
        else:
            temp = {}
            articles = []
            for count, i in enumerate(parents.iter()):
                if i.tag == 'p':
                    articles.append(temp)
                    temp = {}
                else:
                    temp.update({i.tag: i.text})
        return articles

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
            parameters.append('p={}'.format(arguments['-s']))

        return parameters



