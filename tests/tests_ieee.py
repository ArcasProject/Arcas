import arcas
import pandas

def test_setup():
    api = arcas.Ieee()
    assert api.standard == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?'

def test_keys():
    api = arcas.Ieee()
    assert api.keys() == ['url', 'key', 'unique_key', 'title', 'author', 'abstract',
                          'doi', 'date', 'journal', 'provenance', 'category']

def test_parameters_and_url_author():
    api = arcas.Ieee()
    parameters = api.parameters_fix(author='Glynatsi')
    assert parameters == ['author=Glynatsi']

    url = api.create_url_search(parameters)
    assert url == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?author=Glynatsi&apikey=Your key here'

def test_parameters_and_url_title():
    api = arcas.Ieee()
    parameters = api.parameters_fix(title='Game')
    assert parameters == ['article_title=Game']

    url = api.create_url_search(parameters)
    assert url == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?article_title=Game&apikey=Your key here'

def test_parameters_and_url_abstract():
    api = arcas.Ieee()
    parameters = api.parameters_fix(abstract='Game')
    assert parameters == ['abstract=Game']

    url = api.create_url_search(parameters)
    assert url == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?abstract=Game&apikey=Your key here'

def test_parameters_and_url_year():
    api = arcas.Ieee()
    parameters = api.parameters_fix(year=2010)
    assert parameters == ['publication_year=2010']

    url = api.create_url_search(parameters)
    assert url == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?publication_year=2010&apikey=Your key here'


def test_parameters_and_url_category():
    api = arcas.Ieee()
    parameters = api.parameters_fix(category='game theory')
    assert parameters == ['index_terms=game theory']

    url = api.create_url_search(parameters)
    assert url == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?index_terms=game theory&apikey=Your key here'

def test_parameters_and_url_journal():
    api = arcas.Ieee()
    parameters = api.parameters_fix(journal='Ieee')
    assert parameters == ['publication_title=Ieee']

    url = api.create_url_search(parameters)
    assert url == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?publication_title=Ieee&apikey=Your key here'

def test_parameters_and_url_record():
    api = arcas.Ieee()
    parameters = api.parameters_fix(records=1)
    assert parameters == ['max_records=1']

    url = api.create_url_search(parameters)
    assert url == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?max_records=1&apikey=Your key here'

def test_parameters_and_url_start():
    api = arcas.Ieee()
    parameters = api.parameters_fix(start=1)
    assert parameters == ['start_record=1']

    url = api.create_url_search(parameters)
    assert url == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?start_record=1&apikey=Your key here'

def test_create_url_search():
    api = arcas.Ieee()
    parameters = api.parameters_fix(title='Nash', journal='Spinger', records=2, start=5)
    url = api.create_url_search(parameters)
    assert url == 'https://ieeexploreapi.ieee.org/api/v1/search/articles?article_title=Nash&publication_title=Spinger&max_records=2&start_record=5&apikey=Your key here'

def test_to_dataframe():
    dummy_article = {'rank': 1, 'access_type': 'LOCKED', 'content_type': 'Journals',
                     'article_number': '000000', 'doi': '10.1000/',
                     'title': 'Title', 'publication_number': 0, 'publication_title': 'IEEE/Journal',
                     'volume': '22', 'issn': '1063-6692', 'publisher': 'IEEE',
                     'citing_paper_count': 4, 'publication_date': 'May. 2010',
                     'index_terms': {'author_terms': {'terms': ['something else',
                     'something']}}, 'pdf_url': 'https://ieeexplore.ieee.org/stamp/0000',
                     'abstract_url': 'https://ieeexplore.ieee.org/xpl/0000',
                     'html_url': 'https://ieeexplore.ieee.org/xpls/0000',
                     'authors': {'authors': [{'full_name': 'N Glynatsi'},
                     {'full_name': 'V Knight',}]}, 'abstract': "Abstract"}

    api = arcas.Ieee()
    article = api.to_dataframe(dummy_article)

    assert isinstance(article, pandas.core.frame.DataFrame)
    assert list(article.columns) == api.keys()
    assert len(article['url']) == 4

    assert article['url'].unique()[0] == 'https://ieeexplore.ieee.org/xpls/0000'
    assert article['key'].unique()[0] == 'Glynatsi2010'
    assert list(article['author'].unique()) == ['N Glynatsi', 'V Knight']
    assert article['title'].unique()[0] == 'Title'
    assert article['abstract'].unique()[0] == 'Abstract'
    assert article['journal'].unique()[0] == 'IEEE/Journal'
    assert article['date'].unique()[0] == 2010