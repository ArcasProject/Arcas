import arcas
import pandas

def test_setup():
    api = arcas.Plos()
    assert api.standard == 'http://api.plos.org/search?q='

def test_keys():
    api = arcas.Plos()
    assert api.keys() == ['url', 'key', 'unique_key', 'title', 'author', 'abstract',
                          'doi', 'date', 'journal', 'provenance', 'score']

def test_parameters_and_url_author():
    api = arcas.Plos()
    parameters = api.parameters_fix(author='Glynatsi')
    assert parameters == ['author:"Glynatsi"']

    url = api.create_url_search(parameters)
    assert url == 'http://api.plos.org/search?q=author:"Glynatsi"'

def test_parameters_and_url_title():
    api = arcas.Plos()
    parameters = api.parameters_fix(title='Game')
    assert parameters == ['title:"Game"']

    url = api.create_url_search(parameters)
    assert url == 'http://api.plos.org/search?q=title:"Game"'

def test_parameters_and_url_abstract():
    api = arcas.Plos()
    parameters = api.parameters_fix(abstract='Game')
    assert parameters == ['abstract:"Game"']

    url = api.create_url_search(parameters)
    assert url == 'http://api.plos.org/search?q=abstract:"Game"'

def test_parameters_and_url_category():
    api = arcas.Plos()
    parameters = api.parameters_fix(category='game theory')
    assert parameters == ['subject:"game theory"']

    url = api.create_url_search(parameters)
    assert url == 'http://api.plos.org/search?q=subject:"game theory"'

def test_parameters_and_url_journal():
    api = arcas.Plos()
    parameters = api.parameters_fix(journal='PLOS ONE')
    assert parameters == ['journal:"PLOS ONE"']

    url = api.create_url_search(parameters)
    assert url == 'http://api.plos.org/search?q=journal:"PLOS ONE"'

def test_parameters_and_url_record():
    api = arcas.Plos()
    parameters = api.parameters_fix(records=1)
    assert parameters == ['rows=1']

    url = api.create_url_search(parameters)
    assert url == 'http://api.plos.org/search?q=rows=1'

def test_parameters_and_url_start():
    api = arcas.Plos()
    parameters = api.parameters_fix(start=1)
    assert parameters == ['start=1']

    url = api.create_url_search(parameters)
    assert url == 'http://api.plos.org/search?q=start=1'

def test_create_url_search():
    api = arcas.Plos()
    parameters = api.parameters_fix(title='Nash', abstract='mixed', records=2, start=5)
    url = api.create_url_search(parameters)
    assert url == 'http://api.plos.org/search?q=title:"Nash"+AND+abstract:"mixed"&rows=2&start=5'

def test_to_dataframe():
    dummy_article = {'response': [],
                    'id': '10.0000/journal.pone.00000',
                    'journal': 'PLOS ONE',
                    'publication_date': '2010-12-12T00:00:00Z',
                    'article_type': 'Research Article',
                    'author_display': ['E Glynatsi', 'V Knight'],
                    'abstract': "Abstract",
                    'title_display': "Title",
                    'score': '10'}
    api = arcas.Plos()
    article = api.to_dataframe(dummy_article)

    assert isinstance(article, pandas.core.frame.DataFrame)
    assert list(article.columns) == api.keys()
    assert len(article['url']) == 2

    assert article['url'].unique()[0] == 'https://doi.org/' + dummy_article['id']
    assert article['key'].unique()[0] == 'Glynatsi2010'
    assert article['title'].unique()[0] == 'Title'
    assert article['abstract'].unique()[0] == 'Abstract'
    assert article['journal'].unique()[0] == 'PLOS ONE'
    assert article['date'].unique()[0] == 2010
    assert article['doi'].unique()[0] == dummy_article['id']