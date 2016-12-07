from arcas.tools import Api
from xml.etree import ElementTree


class Plos(Api):
    """
     API argument is 'plot'.
    """
    def __init__(self):
        self.standard = 'http://api.plos.org/search?q='

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:]:
            if 'rows=' or 'start=' not in i:
                url += '+AND+{}'.format(i)
            else:
                url += '&{}'.format(i)
        return url

    def to_json(self, article):
        """A function which takes a dictionary with structure of the PLOS
        results and transform it to a standardized format.
        """
        article['author'] = []
        for i in article['authors'].split(';  '):
            article['author'].append({'name': i})
        article['key_word'] = []
        for j in article['term'].split(','):
            article['key_word'].append({'key_word': j})

        article['date'] = {'year': int(article['py'])}
        article['journal'] = article.pop('pubtitle')
        article['pages'] = '{}-{}'.format(article['spage'], article['epage'])
        article['provenance'] = 'PLOS'
        article['read'] = False
        article['labels'], article['list_strategies'] = [], []

        article['key'], article['unique_key'] = self.create_keys(article)
        post = {key: article[key] for key in self.keys()}

        return post

    @staticmethod
    def parse(root):
        """Removing unwanted branches."""
        parents = root.getchildren()
        if not parents:
            articles = False
        else:
            temp = {}
            articles = []
            for count, i in enumerate(parents[0].iter()):
                if (count + 1) % 15 == 0:
                    articles.append(temp)
                    temp = {}
                else:
                    temp.update({i.tag: i.text})
        print(articles)
        return articles

    @staticmethod
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('author:{}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('title:{}'.format(arguments['-t']))
        if arguments['-b'] is not None:
            parameters.append('abstract:{}'.format(arguments['-b']))
        if arguments['-y'] is not None:
            parameters.append('publication_date:[{0}-01-01T00:00:00Z TO '
                              '{0}-12-30T23:59:59Z]'
                              .format(arguments['-y']))
        if arguments['-r'] is not None:
            parameters.append('rows={}'.format(arguments['-r']))
        if arguments['-s'] is not None:
            parameters.append('start={}'.format(arguments['-s']))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root

