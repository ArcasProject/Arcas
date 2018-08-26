import arcas
import pandas

def test_setup():
    api = arcas.Nature()
    assert api.standard == 'http://www.nature.com/opensearch/request?&query='

def test_keys():
    api = arcas.Nature()
    assert api.keys() == ['url', 'key', 'unique_key', 'title', 'author', 'abstract',
                          'doi', 'date', 'journal', 'provenance', 'category', 'score']

def test_parameters_and_url_author():
    api = arcas.Nature()
    parameters = api.parameters_fix(author='Glynatsi')
    assert parameters == ['dc.creator=Glynatsi']

    url = api.create_url_search(parameters)
    assert url == 'http://www.nature.com/opensearch/request?&query=dc.creator=Glynatsi'

def test_parameters_and_url_title():
    api = arcas.Nature()
    parameters = api.parameters_fix(title='Game')
    assert parameters == ['dc.title adj Game']

    url = api.create_url_search(parameters)
    assert url == 'http://www.nature.com/opensearch/request?&query=dc.title adj Game'

def test_parameters_and_url_abstract():
    api = arcas.Nature()
    parameters = api.parameters_fix(abstract='Game')
    assert parameters == ['dc.description adj Game']

    url = api.create_url_search(parameters)
    assert url == 'http://www.nature.com/opensearch/request?&query=dc.description adj Game'

def test_parameters_and_url_year():
    api = arcas.Nature()
    parameters = api.parameters_fix(year=2010)
    assert parameters == ['prism.publicationDate=2010']

    url = api.create_url_search(parameters)
    assert url == 'http://www.nature.com/opensearch/request?&query=prism.publicationDate=2010'

def test_parameters_and_url_category():
    api = arcas.Nature()
    parameters = api.parameters_fix(category='game theory')
    assert parameters == ['dc.subject adj game theory']

    url = api.create_url_search(parameters)
    assert url == 'http://www.nature.com/opensearch/request?&query=dc.subject adj game theory'

def test_parameters_and_url_journal():
    api = arcas.Nature()
    parameters = api.parameters_fix(journal='Nature')
    assert parameters == ['prism.publicationName=Nature']

    url = api.create_url_search(parameters)
    assert url == 'http://www.nature.com/opensearch/request?&query=prism.publicationName=Nature'

def test_parameters_and_url_record():
    api = arcas.Nature()
    parameters = api.parameters_fix(records=1)
    assert parameters == ['maximumRecords=1']

    url = api.create_url_search(parameters)
    assert url == 'http://www.nature.com/opensearch/request?&query=maximumRecords=1'

def test_parameters_and_url_start():
    api = arcas.Nature()
    parameters = api.parameters_fix(start=1)
    assert parameters == ['startRecord=1']

    url = api.create_url_search(parameters)
    assert url == 'http://www.nature.com/opensearch/request?&query=startRecord=1'

def test_create_url_search():
    api = arcas.Nature()
    parameters = api.parameters_fix(title='Nash', abstract='mixed', records=2, start=5)
    url = api.create_url_search(parameters)
    assert url == 'http://www.nature.com/opensearch/request?&query=dc.title adj Nash+AND+dc.description adj mixed&maximumRecords=2&startRecord=5'

def test_to_dataframe():
    dummy_article = {'records': None, 'record': None, 'recordSchema': 'info:srw/schema/11/pam-v2.1',
                     'recordPacking': 'packed', 'recordData': None, 'message': None,
                     'article': None, 'head': None, 'identifier': 'doi:10.1000',
                     'title': 'Title', 'creator': 'E Glynatsi, V Knight',
                     'publicationName': 'Journal', 'doi': '10.1000', 'publicationDate': '2010',
                     'description': 'Abstract',
                     'volume': '48', 'number': '4', 'startingPage': '423',
                     'endingPage': '432', 'url': 'http://nature.org/abs/0000'}

    api = arcas.Nature()
    article = api.to_dataframe(dummy_article)

    assert isinstance(article, pandas.core.frame.DataFrame)
    assert list(article.columns) == api.keys()
    assert len(article['url']) == 2

    assert article['url'].unique()[0] == 'http://nature.org/abs/0000'
    assert article['key'].unique()[0] == 'Glynatsi2010'
    assert article['title'].unique()[0] == 'Title'
    assert article['abstract'].unique()[0] == 'Abstract'
    assert article['journal'].unique()[0] == 'Journal'
    assert article['doi'].unique()[0] == '10.1000'
    assert article['category'].unique()[0] == None
    assert article['score'].unique()[0] == 'Not available'