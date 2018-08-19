import unittest
import requests_mock
from hypothesis import given
import hypothesis.strategies as st
import pandas as pd
from xml.etree.ElementTree import Element
from arcas.tools import Api

article = {'title': 'A Title', 'abstract': 'The Abstract', 'date':  2016,
           'author': ['Author']}


class TestTools(unittest.TestCase):

    def setUp(self):
        standard = 'http:/Search;'
        self.api = Api(standard)

    @given(st.lists(st.text(), min_size=2, max_size=5))
    def test_create_url(self, ls):
        parameters = list(ls)
        url = self.api.create_url_search(parameters)
        assert isinstance(url, str)

    @requests_mock.mock()
    @given(text=st.text())
    def test_requests(self, m, text):
        url = 'http://example.com'
        m.register_uri('GET', url, text=text)
        response = self.api.make_request(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, text)

    def test_xml_to_dict(self):
        root = Element('top')
        children = [Element('child')]
        root.extend(children)

        dummy_dict = self.api.xml_to_dict(root)
        self.assertEqual(type(dummy_dict), dict)

    def test_create_keys(self):
        key, unique_key = self.api.create_keys(article)
        self.assertEqual(key, 'Author2016')
        self.assertEqual(len(unique_key), 32)
        assert isinstance(unique_key, str)
