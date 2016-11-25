import unittest
import collections
import requests
import requests_mock
from xml.etree.ElementTree import Element
from scraping.tools import Api


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

