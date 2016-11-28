import unittest
import collections
import requests
import requests_mock
from xml.etree.ElementTree import Element
from Arcas.tools import Api
from Arcas.IEEE.main import Ieee
from Arcas.arXiv.main import Arxiv

arxiv_entry = dict(
                   {'{http://arxiv.org/schemas/atom}affiliation': 'A',
                    '{http://arxiv.org/schemas/atom}author': 'B',
                    '{http://arxiv.org/schemas/atom}category': None,
                    '{http://arxiv.org/schemas/atom}comment': '8 pages',
                    '{http://arxiv.org/schemas/atom}doi': '10.10.10',
                    '{http://arxiv.org/schemas/atom}entry': '132',
                    '{http://arxiv.org/schemas/atom}id': 'http://arxiv.org/',
                    '{http://arxiv.org/schemas/atom}journal_ref': '',
                    '{http://arxiv.org/schemas/atom}link': None,
                    '{http://arxiv.org/schemas/atom}name': 'C',
                    '{http://arxiv.org/schemas/atom}primary_category': None,
                    '{http://arxiv.org/schemas/atom}published': '2016',
                    '{http://arxiv.org/schemas/atom}summary': 'Summary',
                    '{http://arxiv.org/schemas/atom}title': 'Title',
                    '{http://arxiv.org/schemas/atom}updated': '2016'})

ieee_entry = dict(
                  {'rank': '1',
                   'title': "Title",
                   'authors': 'A',
                   'affiliations': 'B',
                   'term': 'C',
                   'term': 'D',
                   'pubtitle': 'E',
                   'punumber': '1',
                   'publisher': 'IEEE',
                   'py': '2016',
                   'spage': '1',
                   'epage': '2',
                   'abstract': "Abstract",
                   'issn': '1234-5678',
                   'doi': '10.10',
                   'publicationId': '1234',
                   'partnum': '1234',
                   'mdurl': 'http://ieeexplore.ieee.org',
                   'pdf': 'http://ieeexplore.ieee.org/'})

keys = ['key', 'unique_key', 'title', 'abstract', 'author', 'date', 'journal',
        'pages', 'labels', 'read', 'key_word', 'provelance', 'list_strategies']


class TestTools(unittest.TestCase):

    def setUp(self):
        standard = 'http:/Search;'
        self.api = Api(standard)

    def test_create_url(self):

        parameters = ['ti=Title', 'au=Author']
        url = self.api.create_url_search(parameters=parameters)
        self.assertEqual('http:/Search;ti=Title&au=Author', url)

    @requests_mock.mock()
    def test_requests(self, m):
        url = "http://example.com"

        m.register_uri('GET', url, text='data')
        response = self.api.make_request(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'data')

    def test_xml_to_dict(self):
        root = Element('top')
        children = [Element('child')]
        root.extend(children)

        dummy_dict = self.api.xml_to_dict(root)
        self.assertEqual(type(dummy_dict), collections.defaultdict)


class TestArxiv(unittest.TestCase):

    def setUp(self):
        self.api = Arxiv()

    def test_to_json(self):
        post = self.api.to_json(arxiv_entry)
        self.assertEqual(sorted(post.keys()), sorted(keys))


class TestIEEE(unittest.TestCase):
    def setUp(self):
        self.api = Ieee()

    def test_to_json(self):
        post = self.api.to_json(ieee_entry)
        self.assertEqual(sorted(post.keys()), sorted(keys))
