import arcas
import pandas

def test_setup():
    api = arcas.Springer()
    assert api.standard == 'http://api.springer.com/metadata/pam?q='

def test_keys():
    api = arcas.Springer()
    assert api.keys() == ['url', 'key', 'unique_key', 'title', 'author', 'abstract',
                          'doi', 'date', 'journal', 'provenance', 'category', 'score']

def test_parameters_and_url_author():
    api = arcas.Springer()
    parameters = api.parameters_fix(author='Glynatsi')
    assert parameters == ['name:Glynatsi']

    url = api.create_url_search(parameters)
    assert url == 'http://api.springer.com/metadata/pam?q=name:Glynatsi&api_key=Your key here'

def test_parameters_and_url_title():
    api = arcas.Springer()
    parameters = api.parameters_fix(title='Game')
    assert parameters == ['title:Game']

    url = api.create_url_search(parameters)
    assert url == 'http://api.springer.com/metadata/pam?q=title:Game&api_key=Your key here'

def test_parameters_and_url_category():
    api = arcas.Springer()
    parameters = api.parameters_fix(category='game theory')
    assert parameters == ['subject:game theory']

    url = api.create_url_search(parameters)
    assert url == 'http://api.springer.com/metadata/pam?q=subject:game theory&api_key=Your key here'

def test_parameters_and_url_journal():
    api = arcas.Springer()
    parameters = api.parameters_fix(journal='Springer')
    assert parameters == ['pub:Springer']

    url = api.create_url_search(parameters)
    assert url == 'http://api.springer.com/metadata/pam?q=pub:Springer&api_key=Your key here'

def test_parameters_and_url_record():
    api = arcas.Springer()
    parameters = api.parameters_fix(records=1)
    assert parameters == ['p=1']

    url = api.create_url_search(parameters)
    assert url == 'http://api.springer.com/metadata/pam?q=p=1&api_key=Your key here'

def test_parameters_and_url_start():
    api = arcas.Springer()
    parameters = api.parameters_fix(start=1)
    assert parameters == ['s=1']

    url = api.create_url_search(parameters)
    assert url == 'http://api.springer.com/metadata/pam?q=s=1&api_key=Your key here'

def test_create_url_search():
    api = arcas.Springer()
    parameters = api.parameters_fix(title='Nash', journal='Spinger', records=2, start=5)
    url = api.create_url_search(parameters)
    assert url == 'http://api.springer.com/metadata/pam?q=title:Nash+AND+pub:Spinger&p=2&s=5&api_key=Your key here'

def test_to_dataframe():
    dummy_article = {'identifier': 'doi:10.1000/', 'title': 'Title',
                     'creator': 'E Glynatsi, V Knight', 'publicationName': 
                     'Awesome Journal', 'genre': 'ReviewPaper', 'openAccess': 'false',
                     'h1': 'Abstract', 'p': 'Abstract',
                     'doi': '10.1000/', 'publisher': 'Springer',
                     'publicationDate': '2021-01-01', 'url': 'http://dx.doi.org/10.1000/'}

    api = arcas.Springer()
    article = api.to_dataframe(dummy_article)

    assert isinstance(article, pandas.core.frame.DataFrame)
    assert list(article.columns) == api.keys()
    assert len(article['url']) == 2

    assert article['url'].unique()[0] == 'http://dx.doi.org/10.1000/'
    assert article['key'].unique()[0] == 'Glynatsi2021'
    assert article['title'].unique()[0] == 'Title'
    assert article['abstract'].unique()[0] == 'Abstract'
    assert article['journal'].unique()[0] == 'Awesome Journal'
    assert article['date'].unique()[0] == 2021
    assert article['score'].unique()[0] == 'Not available'