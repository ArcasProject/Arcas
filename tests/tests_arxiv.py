import arcas
import pandas

def test_setup():
    api = arcas.Arxiv()
    assert api.standard == 'http://export.arxiv.org/api/query?search_query='

def test_keys():
    api = arcas.Arxiv()
    assert api.keys() == ['url', 'key', 'unique_key', 'title', 'author',
                          'abstract', 'doi', 'date', 'journal', 'provenance',
                          'primary_category', 'category']

def test_parameters_and_url_author():
    api = arcas.Arxiv()
    parameters = api.parameters_fix(author='Glynatsi')
    assert parameters == ['au:Glynatsi']

    url = api.create_url_search(parameters)
    assert url == 'http://export.arxiv.org/api/query?search_query=au:Glynatsi'

def test_parameters_and_url_title():
    api = arcas.Arxiv()
    parameters = api.parameters_fix(title='Game')
    assert parameters == ['ti:Game']

    url = api.create_url_search(parameters)
    assert url == 'http://export.arxiv.org/api/query?search_query=ti:Game'

def test_parameters_and_url_abstract():
    api = arcas.Arxiv()
    parameters = api.parameters_fix(abstract='Game')
    assert parameters == ['abs:Game']

    url = api.create_url_search(parameters)
    assert url == 'http://export.arxiv.org/api/query?search_query=abs:Game'

def test_parameters_and_url_category():
    api = arcas.Arxiv()
    parameters = api.parameters_fix(category='game theory')
    assert parameters == ['cat:game theory']

    url = api.create_url_search(parameters)
    assert url == 'http://export.arxiv.org/api/query?search_query=cat:game theory'

def test_parameters_and_url_journal():
    api = arcas.Arxiv()
    parameters = api.parameters_fix(journal='arxiv')
    assert parameters == ['jr:arxiv']

    url = api.create_url_search(parameters)
    assert url == 'http://export.arxiv.org/api/query?search_query=jr:arxiv'

def test_parameters_and_url_record():
    api = arcas.Arxiv()
    parameters = api.parameters_fix(records=1)
    assert parameters == ['max_results=1']

    url = api.create_url_search(parameters)
    assert url == 'http://export.arxiv.org/api/query?search_query=max_results=1'

def test_parameters_and_url_start():
    api = arcas.Arxiv()
    parameters = api.parameters_fix(start=1)
    assert parameters == ['start=1']

    url = api.create_url_search(parameters)
    assert url == 'http://export.arxiv.org/api/query?search_query=start=1'

def test_create_url_search():
    api = arcas.Arxiv()
    parameters = api.parameters_fix(title='Nash', abstract='mixed', records=2, start=5)
    url = api.create_url_search(parameters)
    assert url == 'http://export.arxiv.org/api/query?search_query=ti:Nash&abs:mixed&max_results=2&start=5'

def test_to_dataframe():
    dummy_article = {'entry': '\n', 'id': 'http://arxiv.org/abs/0000',
                     'updated': '2011', 'published': '2010', 'title': 'Title',
                     'summary': "Abstract", 'author': '\n', 'name': 'E Glynatsi, V Knight',
                     'doi': '10.0000', 'comment': 'This is a comment.',
                     'journal_ref': 'Awesome Journal', 'primary_category': 'Dummy',
                     'category': None}
    api = arcas.Arxiv()
    article = api.to_dataframe(dummy_article)

    assert isinstance(article, pandas.core.frame.DataFrame)
    assert list(article.columns) == api.keys()
    assert len(article['url']) == 2

    assert article['url'].unique()[0] == 'http://arxiv.org/abs/0000'
    assert article['key'].unique()[0] == 'Glynatsi2010'
    assert article['title'].unique()[0] == 'Title'
    assert article['abstract'].unique()[0] == 'Abstract'
    assert article['journal'].unique()[0] == 'Awesome Journal'
    assert article['primary_category'].unique()[0] == 'Dummy'
    assert article['category'].unique()[0] == None