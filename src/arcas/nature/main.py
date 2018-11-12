from arcas.tools import Api
from xml.etree import ElementTree


class Nature(Api):
    def __init__(self):
        self.standard = 'http://www.nature.com/opensearch/request?&query='

    def create_url_search(self, parameters):
        """Creates the search url, combining the standard url and various
        search parameters."""
        url = self.standard
        url += parameters[0]
        for i in parameters[1:]:
            if 'maximumRecords=' in i or 'startRecord=' in i:
                url += '&{}'.format(i)
            else:
                url += '+AND+{}'.format(i)
        return url

    @staticmethod
    def xml_to_dict(records):
        """Xml response with information on article to dictionary"""
        d = {}
        for key, value in records:
            if key not in d:
                d[key] = value
            else:
                value = value.replace(',', ' ')
                d[key] += ',' + value
        return d

    def parse(self, root):
        """Parsing the xml file"""
        parents = root.getchildren()
        diagnostics = parents[3].tag.split('}')[-1]
        number_of_records = parents[0].text
        if (diagnostics == 'diagnostics') or (number_of_records == '0'):
            return False
        else:
            parents = parents[2]
            raw_articles = [[]]
            for at in parents.iter():
                key = at.tag.split('}')[-1]
                if key == 'recordPosition':
                    raw_articles.append([])
                else:
                   raw_articles[-1].append((key, at.text))

            while [] in raw_articles:
                raw_articles.remove([])

        return [self.xml_to_dict(raw_article) for raw_article in raw_articles]

    def to_dataframe(self, raw_article):
        """A function which takes a dictionary with structure of the nature
        results and transform it to a standardized format.
        """
        raw_article['url'] = raw_article.get('url', None)
        for key_one, key_two in [['author', 'creator'], ['category', 'subject']]:
            raw_article[key_one] = raw_article.get(key_two, None)
            if raw_article[key_one] is not None:
                raw_article[key_one] = raw_article[key_one].split(',')
        if raw_article['author'] is None:
            raw_article['author'] = ['No authors found for this document.']

        raw_article['abstract'] = raw_article.get('description', None)
        raw_article['date'] = int(raw_article.get('publicationDate', '0').split('-')[0])
        raw_article['journal'] = raw_article.get('publicationName', None)

        raw_article['category'] = raw_article.get('subject', None)
        if raw_article['category'] is not None:
            raw_article['category'] = raw_article['category'].split(',')

        raw_article['provenance'] = 'Nature'
        raw_article['title'] = raw_article.get('title', None)
        raw_article['doi'] = raw_article.get('doi', None)
        raw_article['key'], raw_article['unique_key'] = self.create_keys(raw_article)

        raw_article['open_access'] = 'Not available'
        raw_article['score'] = 'Not available'
        return self.dict_to_dataframe(raw_article)

    @staticmethod
    def parameters_fix(author=None, title=None, abstract=None, year=None,
                       records=None, start=None, category=None, journal=None,
                       keyword=None):
        parameters = []
        if author is not None:
            parameters.append('dc.creator={}'.format(author))
        if title is not None:
            parameters.append('dc.title adj {}'.format(title))
        if abstract is not None:
            parameters.append('dc.description adj {}'.format(abstract))
        if year is not None:
            parameters.append('prism.publicationDate={}'.format(year))
        if journal is not None:
            parameters.append('prism.publicationName={}'.format(journal))
        if category is not None:
            parameters.append('dc.subject adj {}'.format(category))
        if keyword is not None:
            parameters.append('cql.keywords={}'.format(keyword))
        if records is not None:
            parameters.append('maximumRecords={}'.format(records))
        if start is not None:
            parameters.append('startRecord={}'.format(start))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root