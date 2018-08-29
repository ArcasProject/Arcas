from xml.etree.ElementTree import Element

import pandas as pd

import requests_mock
from arcas.tools import Api

standard = 'http:/Search;'

def test_api():
    api =  Api(standard)
    assert api.standard == standard

def test_create_url():
    parameters = ['title=game', 'year=2010', 'author=N Glynatsi']
    api =  Api(standard)

    url = api.create_url_search(parameters)
    assert isinstance(url, str)
    for parameter in parameters:
        assert parameter in url

def test_requests():
    with requests_mock.mock() as m:
        url = 'http://example.com'
        m.register_uri('GET', url, text='Example text')
        api = Api(url)
        response = api.make_request(url)

        assert response.status_code == 200
        assert response.text == 'Example text'

def test_xml_to_dict():
    root = Element('top')
    children = [Element('child')]
    root.extend(children)

    api = Api(standard)
    
    dummy_dict = api.xml_to_dict(root)
    assert isinstance(dummy_dict, dict)

def test_create_keys():
    article = {'title': 'A Title', 'abstract': 'The Abstract', 'date':  2000,
               'author': ['Author']}
    api = Api(standard)
    key, unique_key = api.create_keys(article)

    assert key == 'Author2000'
    assert len(unique_key) == 32
    assert isinstance(unique_key, str)
