from arcas.tools import Api
from xml.etree import ElementTree


class Plos(Api):
    """
     API argument is 'plot'.
    """
    def __init__(self):
        self.standard = 'http://api.plos.org/search?q='

    @staticmethod
    def keys():
        """
        Fields we are keeping from Springer results.
        """
        keys = ['key', 'unique_key', 'title', 'author', 'abstract',
                'date', 'journal', 'provenance', 'score']
        return keys

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:]:
            if 'rows=' in i or 'start=' in i:
                url += '&{}'.format(i)
            else:
                url += '+AND+{}'.format(i)
        return url

    def to_dataframe(self, raw_article):
        """A function which takes a dictionary with structure of the PLOS
        results and transform it to a standardized format.
        """
        raw_article['author'] = raw_article.get('author_display', None)
        try:
            raw_article['abstract'] = raw_article.get('abstract', [None])[0]
        except IndexError:
            raw_article['abstract'] = None

        raw_article['date'] = int(raw_article.get('publication_date', '0').split('-')[0])
        raw_article['journal'] = raw_article.get('journal', None)
        raw_article['provenance'] = 'PLOS'
        raw_article['score'] = raw_article.get('score', None)
        raw_article['title'] = raw_article.get('title_display', None)
        raw_article['key'], raw_article['unique_key'] = self.create_keys(
            raw_article)

        return self.dict_to_dataframe(raw_article)

    @staticmethod
    def xml_to_dict(record):
        """Xml response with information on article to dictionary"""
        d = {}
        for key, value in record:
            if key is not None:
                if value is not None:
                    d[key] = value
                else:
                    d[key] = []
                    current_key = key
            else:
                if value is not None:
                    d[current_key].append(value)
        return d

    def parse(self, root):
        """Parsing the xml file"""
        parents = root.getchildren()
        if len(parents[0]) == 0:
            return False
        else:
            raw_articles = [[]]
            for at in parents[0].iter():
                try:
                    key = list(at.attrib.values())[0]
                except IndexError:
                    key = None
                if key == 'score':
                    raw_articles[-1].append((key, at.text))
                    raw_articles.append([])
                else:
                    raw_articles[-1].append((key, at.text))
            while [] in raw_articles:
                raw_articles.remove([])

        return [self.xml_to_dict(raw_article) for raw_article in raw_articles]

    @staticmethod
    def parameters_fix(author=None, title=None, abstract=None, year=None,
                       records=None, start=None):
        parameters = []
        if author is not None:
            parameters.append('author:{}'.format(author))
        if title is not None:
            parameters.append('title:{}'.format(title))
        if abstract is not None:
            parameters.append('abstract:{}'.format(abstract))
        if year is not None:
            parameters.append('publication_date:[{0}-01-01T00:00:00Z TO '
                              '{0}-12-30T23:59:59Z]'
                              .format(year))
        if records is not None:
            parameters.append('rows={}'.format(records))
        if start is not None:
            parameters.append('start={}'.format(start))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root

