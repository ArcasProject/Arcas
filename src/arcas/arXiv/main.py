from arcas.tools import Api
from xml.etree import ElementTree


class Arxiv(Api):
    def __init__(self):
        self.standard = 'http://export.arxiv.org/api/query?search_query='

    @staticmethod
    def keys():
        """
        Fields we are keeping from arXiv results.
        """
        keys = ['url', 'key', 'unique_key', 'title', 'author', 'abstract', 'doi',
                'date', 'journal', 'provenance', 'primary_category', 'category',
                'score', 'open_access']
        return keys

    def to_dataframe(self, raw_article):
        """A function which takes a dictionary with structure of the arXiv
        results, transforms it to a standardized format and returns a dataframe.
        """
        raw_article['url'] = raw_article.get('id', None)

        for key_one, key_two in [['author', 'name'], ['category', 'category']]:
            raw_article[key_one] = raw_article.get(key_two, None)
            if raw_article[key_one] is not None:
                raw_article[key_one] = raw_article[key_one].split(',')

        raw_article['abstract'] = raw_article.get('summary', None)
        raw_article['date'] = int(raw_article.get('published', '0').split('-')[0])
        raw_article['journal'] = raw_article.get('journal_ref', None)
        if raw_article['journal'] is None:
            raw_article['journal'] = "arXiv"

        raw_article['provenance'] = 'arXiv'
        raw_article['title'] = raw_article.get('title', None)
        raw_article['doi'] = raw_article.get('doi', None)
        raw_article['key'], raw_article['unique_key'] = self.create_keys(raw_article)

        raw_article['open_access'] = True
        raw_article['score'] = 'Not available'
        return self.dict_to_dataframe(raw_article)

    def parse(self, root):
        """Removing unwanted branches."""
        branches = root.getchildren()
        raw_articles = []
        for record in branches:
            if 'entry' in record.tag:
                raw_articles.append(self.xml_to_dict(record))
        if not raw_articles:
            raw_articles = False
        return raw_articles

    @staticmethod
    def parameters_fix(author=None, title=None, abstract=None, year=None,
                       records=None, start=None, category=None, journal=None,
                       keyword=None):
        parameters = []
        if author is not None:
            parameters.append('au:{}'.format(author))
        if title is not None:
            parameters.append('ti:{}'.format(title))
        if abstract is not None:
            parameters.append('abs:{}'.format(abstract))
        if category is not None:
            parameters.append('cat:{}'.format(category))
        if journal is not None:
            parameters.append('jr:{}'.format(journal))
        if keyword is not None:
            parameters.append('all:{}'.format(keyword))
        if records is not None:
            parameters.append('max_results={}'.format(records))
        if start is not None:
            parameters.append('start={}'.format(start))
        if year is not None:
            print('ArXiv does not support argument year.') # TODO: Add url to documentation

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root
