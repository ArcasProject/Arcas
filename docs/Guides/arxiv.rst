How to ping ArXiv
================

arXiv is set as the default api for arcas. For more information on interacting with the
api visit the official site for the user's manual: https://arxiv.org/help/api/user-manual.

arXiv supports the following arguments as search fields:

- :code:`author`
- :code:`title`
- :code:`abstract`
- :code:`category`
- :code:`journal`
- :code:`records`
- :code:`start`

Note that :code:`year` is not support by the arXiv API. Let us consider an example where
we would like to retrieve the metadata of single article with the word "Game" in the
:code:`title` which belongs in the :code:`category` "game theory" and it was published
on arXiv.

Initially, we import Arcas and make an :code:`Arxiv()` instance::

    >>> import arcas
    >>> api = arcas.Arxiv()

Secondly we create the parameters list will be used to generate our message to the
API::

    >>> parameters = api.parameters_fix(title='Game', category='game theory', records=1)
    >>> url = api.create_url_search(parameters)
    >>> url
    'http://export.arxiv.org/api/query?search_query=ti:Game&cat:game theory&max_results=1'

The url then is used to obtain a relevant article::

    >>> request = api.make_request(url)
    >>> root = api.get_root(request)
    >>> raw_article = api.parse(root)
    >>> article = api.to_dataframe(*raw_article)

The :code:`Arxiv()` class returns the following results::

    >>> article.columns
    Index(['url', 'key', 'unique_key', 'title', 'author', 'abstract', 'doi',
        'date', 'journal', 'provenance', 'primary_category', 'category'],
        dtype='object')