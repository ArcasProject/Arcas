.. _tutorial-i:

=======================================
Tutorial I: Retrieving a single article
=======================================

In this tutorial the aim is to retrieve a single article for the journal
arXiv, where the word 'Game' is contained in the title or the abstract.

Initially, let us import Arcas::

    >>> import arcas

The APIs, are implemented as classes. Here we make an API instance of the API
arXiv::

    >>> api = arcas.Arxiv()

We will now create the query, to which arXiv listens to. :code:`records` is the
number of records we are requesting for::

    >>> parameters = api.parameters_fix(title='Game', abstract='Game', records=1)
    >>> url = api.create_url_search(parameters)

The query will be used to ping the API and afterwards we parse the xml file
that has been retrieved::

    >>> request = api.make_request(url)
    >>> root = api.get_root(request)
    >>> raw_article = api.parse(root)
    >>> article = api.to_dataframe(raw_article[0])

Note that we are using the library `pandas <http://pandas.pydata.org/>`_ to
store the results. The data frame contains metadata on an article as they
are recorded in the journal arXiv. Here we can type the following to see the
columns of the data frame::

    >>> article.columns
    Index(['key', 'unique_key', 'title', 'author', 'abstract', 'date', 'journal',
           'pages', 'key_word', 'provenance'],dtype='object')

and we can ask for the title::

    >>> article.title.unique()
        array([ 'A New Approach to Solve a Class of Continuous-Time Nonlinear
        Quadratic Zero-Sum Game Using ADP'], dtype=object)

The structure of the results is discussed in depth in :ref:`result set<results-set>`.