from arcas.tools import Api
from xml.etree import ElementTree


class Arxiv(Api):
    """
     API argument is 'ieee'.
    """
    def __init__(self):
        self.standard = 'http://export.arxiv.org/api/query?search_query='

    @staticmethod
    def keys():
        """
        Fields we are keeping from arXiv results.
        """
        keys = ['key', 'unique_key', 'title', 'author', 'abstract',
                'date', 'journal', 'provenance']
        return keys

    def to_dataframe(self, raw_article):
        """A function which takes a dictionary with structure of the arXiv
        results and transform it to a standardized format.
        """
        raw_article = {k.split('}')[-1]: v for k, v in raw_article.items()}

        raw_article['author'] = raw_article.get('name', None)
        if raw_article['author'] is not None:
            raw_article['author'] = raw_article['author'].split(',')

        raw_article['abstract'] = raw_article.get('summary', None)
        raw_article['date'] = int(raw_article.get('published', '0').split('-')[0])
        raw_article['journal'] = raw_article.get('journal_ref', None)
        if raw_article['journal'] is None:
            raw_article['journal'] = "arXiv"

        raw_article['provenance'] = 'arXiv'
        raw_article['title'] = raw_article.get('title', None)
        raw_article['key'], raw_article['unique_key'] = self.create_keys(
            raw_article)

        return self.dict_to_dataframe(raw_article)

    def parse(self, root):
        """Removing unwanted branches."""
        parents = root.getchildren()
        raw_articles = []
        for _ in range(7):
            parents.remove(parents[0])
        if not parents:
            raw_articles = False
        else:
            for record in parents:
                raw_articles.append(self.xml_to_dict(record))
        return raw_articles

    @staticmethod
    def parameters_fix(author=None, title=None, abstract=None, year=None,
                       records=None, start=None):
        parameters = []
        if author is not None:
            parameters.append('au:{}'.format(author))
        if title is not None:
            parameters.append('ti:{}'.format(title))
        if abstract is not None:
            parameters.append('abs:{}'.format(abstract))
        if records is not None:
            parameters.append('max_results={}'.format(records))
        if start is not None:
            parameters.append('start={}'.format(start))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root
