from arcas.tools import Api
import xml.etree.ElementTree as etree
from xml.etree import ElementTree


class Plos(Api):
    def __init__(self):
        self.standard = 'http://api.plos.org/search?q='

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
        raw_article['abstract'] = raw_article.get('abstract', [None])

        raw_article['date'] = int(raw_article.get('publication_date', '0').split('-')[0])
        raw_article['journal'] = raw_article.get('journal', None)
        raw_article['provenance'] = 'PLOS'
        raw_article['score'] = raw_article.get('score', None)
        if raw_article['score'] is not None:
            raw_article['score'] = int(raw_article['score'])
        raw_article['doi'] = raw_article.get('id', None)
        raw_article['url'] = 'https://doi.org/' + raw_article['id']
        raw_article['title'] = raw_article.get('title_display', None)
        raw_article['key'], raw_article['unique_key'] = self.create_keys(raw_article)

        raw_article['category'] = 'Not available'
        raw_article['open_access'] = 'Not available'
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
        if root['response']['numFound'] == 0:
            return False
        return root['response']['docs']

    @staticmethod
    def parameters_fix(author=None, title=None, abstract=None, year=None,
                       records=None, start=None, category=None, journal=None,
                       keyword=None):
        parameters = []
        if author is not None:
            parameters.append('author:"{}"'.format(author))
        if title is not None:
            parameters.append('title:"{}"'.format(title))
        if abstract is not None:
            parameters.append('abstract:"{}"'.format(abstract))
        if year is not None:
            parameters.append('publication_date:[{0}-01-01T00:00:00Z TO '
                              '{0}-12-30T23:59:59Z]'.format(year))
        if journal is not None:
            parameters.append('journal:"{}"'.format(journal))
        if category is not None:
            parameters.append('subject:"{}"'.format(category))
        if keyword is not None:
            parameters.append('everything:"{}"'.format(keyword))
        if records is not None:
            parameters.append('rows={}'.format(records))
        if start is not None:
            parameters.append('start={}'.format(start))

        return parameters

    @staticmethod
    def get_root(response):
        root = response.json()
        return root

