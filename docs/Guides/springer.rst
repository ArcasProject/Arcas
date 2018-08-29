How to ping Springer
================

For more information on interacting with the Springer api visit the official
site for the user's manual: https://dev.springernature.com/.

In order to use Sringer api you will need to sign up and create an application
key. You can sign up in the following https://dev.springernature.com/. Once
you have done that you will need to copy the key in the `api_key.py`. This
is located in the folder `src/arcas/Springer`.

Once this is done you are all set to interact with the api. Springer supports
the following arguments as search fields:

- :code:`author`
- :code:`title`
- :code:`journal`
- :code:`category`
- :code:`records`
- :code:`start`

Note that `abstract` is not supported. Let us consider an example where
we would like to retrieve the metadata of single article with the word "Game" in the
:code:`title` published on :code:`year` 2010.

Initially, we import Arcas and make an :code:`Springer()` instance::

    >>> import arcas
    >>> api = arcas.Springer()

Secondly we create the parameters list will be used to generate our message to the
API::

    >>> parameters = api.parameters_fix(title='Game', year=2010, records=1)
    >>> url = api.create_url_search(parameters)
    >>> url
    'http://api.springer.com/metadata/pam?q=title:Game+AND+year:2010+AND+subject:game theory&p=1&api_key=Your key here'

The url then is used to obtain a relevant article::

    >>> request = api.make_request(url)
    >>> root = api.get_root(request)
    >>> raw_article = api.parse(root)
    >>> article = api.to_dataframe(*raw_article)

The :code:`Springer()` class returns the following results::

    >>> article.columns
    Index(['url', 'key', 'unique_key', 'title', 'author', 'abstract', 'doi',
       'date', 'journal', 'provenance'],
      dtype='object')