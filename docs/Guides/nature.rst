How to ping Nature
================
For more information on interacting with the api's visit the official site:
https://www.nature.com/opensearch/.

Nature supports the following arguments as search fields:

- :code:`author`
- :code:`title`
- :code:`abstract`
- :code:`category`
- :code:`journal`
- :code:`year`
- :code:`records`
- :code:`start`

Let us consider an example where we would like to retrieve the metadata of single
article with the word "Game" in the :code:`title` which was published by the
:code:`journal` "Journal of the Operational Research Society".

Initially, we import Arcas and make an :code:`Nature()` instance::

    >>> import arcas
    >>> api = arcas.Nature()

Secondly we create the parameters list will be used to generate our message to the
API::

    >>> parameters = api.parameters_fix(title='Game', journal='Journal of the Operational Research Society', records=1)
    >>> url = api.create_url_search(parameters)
    >>> url
    'http://www.nature.com/opensearch/request?&query=dc.title adj Game+AND+prism.publicationName=Journal of the Operational Research Society&maximumRecords=1'

The url then is used to obtain a relevant article::

    >>> request = api.make_request(url)
    >>> root = api.get_root(request)
    >>> raw_article = api.parse(root)
    >>> article = api.to_dataframe(*raw_article)

The :code:`Nature()` class returns the following results::

    >>> article.columns
    Index(['url', 'key', 'unique_key', 'title', 'author', 'abstract', 'doi',
       'date', 'journal', 'provenance', 'category'],
      dtype='object')