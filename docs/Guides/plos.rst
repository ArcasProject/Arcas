How to ping Plos
================

For more information on  PLOS Search API visit the official site: http://api.plos.org/solr/faq/.

arXiv supports the following arguments as search fields:

- :code:`author`
- :code:`title`
- :code:`abstract`
- :code:`category`
- :code:`journal`
- :code:`year`
- :code:`records`
- :code:`start`

Let us consider an example where we would like to retrieve the metadata of single article
with the word "Game" in the :code:`title` which belongs in the :code:`category`
"game theory" and it was published on PLOS ONE.

Initially, we import Arcas and make an :code:`Plos()` instance::

    >>> import arcas
    >>> api = arcas.Plos()

Secondly we create the parameters list will be used to generate our message to the
API::

    >>> parameters = api.parameters_fix(title='Game', category='game theory', records=1)
    >>> url = api.create_url_search(parameters)
    >>> url
    'http://api.plos.org/search?q=title:"Game"+AND+subject:"game theory"&rows=1'

The url then is used to obtain a relevant article::

    >>> request = api.make_request(url)
    >>> root = api.get_root(request)
    >>> raw_article = api.parse(root)
    >>> article = api.to_dataframe(*raw_article)

The :code:`Plos()` class returns the following results::

    >>> article.columns
    Index(['url', 'key', 'unique_key', 'title', 'author', 'abstract', 'doi',
        'date', 'journal', 'provenance', 'score'],
        dtype='object')