from arcas.tools import Api
from .api_key import api_key
from xml.etree import ElementTree


class Springer(Api):
    """
     API argument is 'springer'.
    """
    def __init__(self):
        self.standard = 'http://api.springer.com/metadata/pam?q='
        self.key_api = api_key

    @staticmethod
    def keys():
        """
        Fields we are keeping from Springer results.
        """
        keys = ['key', 'unique_key', 'title', 'author', 'abstract',
                'date', 'journal', 'provenance']
        return keys

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:]:
            if 's=' in i or 'p=' in i:
                url += '&{}'.format(i)
            else:
                url += '+AND+{}'.format(i)
        url += '&api_key={}'.format(self.key_api)
        return url

    def to_dataframe(self, raw_article):
        """A function which takes a dictionary with structure of the Springer
        results and transform it to a standardized format.
        """
        raw_article['author'] = raw_article.get('creator', None)
        if raw_article['author'] is not None:
            raw_article['author'] = raw_article['author'].split(',')

        raw_article['abstract'] = raw_article.get('p', None)
        raw_article['date'] = int(raw_article.get('publicationDate', '0').split('-')[
                                  0])
        raw_article['journal'] = raw_article.get('publicationName', None)
        raw_article['provenance'] = 'Springer'
        raw_article['title'] = raw_article.get('title', None)
        raw_article['key'], raw_article['unique_key'] = self.create_keys(
            raw_article)

        return self.dict_to_dataframe(raw_article)

    @staticmethod
    def xml_to_dict(raw_article):
        """Xml response with information on article to dictionary"""
        d = {}
        for key, value in raw_article:
            if key not in d:
                if value is not None:
                    value = value.replace(',', ' ')
                    d[key] = value
            else:
                if value is not None:
                    value = value.replace(',', ' ')
                    d[key] += ',' + value
        return d

    def parse(self, root):
        """Parsing the xml file"""
        parents = root.getchildren()[3]
        if not parents:
            return False
        else:
            raw_articles = [[]]
            for at in parents.iter():
                key = at.tag.split('}')[-1]
                if key == 'article':
                    raw_articles.append([])
                else:
                    raw_articles[-1].append((key, at.text))
            raw_articles.remove(raw_articles[0])
            while [] in raw_articles:
                raw_articles.remove([])
        return [self.xml_to_dict(raw_article) for raw_article in raw_articles]

    @staticmethod
    def parameters_fix(author=None, title=None, abstract=None, year=None,
                       records=None, start=None):
        parameters = []
        if author is not None:
            parameters.append('name:{}'.format(author))
        if title is not None:
            parameters.append('title:{}'.format(title))
        if year is not None:
            parameters.append('year:{}'.format(year))
        if records is not None:
            parameters.append('p={}'.format(records))
        if start is not None:
            parameters.append('s={}'.format(start))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root


