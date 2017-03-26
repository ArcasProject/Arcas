from arcas.tools import Api


class Ieee(Api):
    """
     API argument is 'ieee'.
    """
    def __init__(self):
        self.standard = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?'

    @staticmethod
    def keys():
        """
        Fields we are keeping from IEEE results.
        """
        keys = ['key', 'unique_key', 'title', 'author', 'abstract',
                'date', 'journal', 'pages', 'key_word', 'provenance']
        return keys

    def to_dataframe(self, raw_article):
        """A function which takes a dictionary with structure of the IEEE
        results and transform it to a standardized format.
        """
        raw_article['author'] = raw_article.get('authors', None)
        if raw_article['author'] is not None:
            raw_article['author'] = raw_article['author'].split('; ')

        raw_article['abstract'] = raw_article.get('abstract', None)
        raw_article['date'] = int(raw_article.get('py', 0))
        raw_article['journal'] = raw_article.get('pubtitle', 'None')
        raw_article['pages'] = '{}-{}'.format(raw_article.get('spage', None),
                                              raw_article.get('epage', None))

        raw_article['key_word'] = raw_article.get('term', None)
        if raw_article['key_word'] is not None:
            raw_article['key_word'] = raw_article['key_word'].split(',')

        raw_article['provenance'] = 'IEEE'
        raw_article['title'] = raw_article.get('title', None)
        raw_article['key'], raw_article['unique_key'] = self.create_keys(
            raw_article)

        return self.dict_to_dataframe(raw_article)

    def parse(self, root):
        """Parsing the xml file"""
        try:
            parents = root.getchildren()
            raw_articles = []
            for _ in range(2):
                parents.remove(parents[0])

            for record in parents:
                raw_articles.append(self.xml_to_dict(record))
        except IndexError:
            raw_articles = False

        return raw_articles

    @staticmethod
    def parameters_fix(author=None, title=None, abstract=None, year=None,
                       records=None, start=None):
        parameters = []
        if author is not None:
            parameters.append('au={}'.format(author))
        if title is not None:
            parameters.append('ti={}'.format(title))
        if abstract is not None:
            parameters.append('ab={}'.format(abstract))
        if year is not None:
            parameters.append('py={}'.format(year))
        if records is not None:
            parameters.append('hc={}'.format(records))
        if start is not None:
            parameters.append('rs={}'.format(start))

        return parameters
