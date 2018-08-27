.. _abstract:

How to: Collect articles' based on `abstract`
============================================

Often we might search articles based on words that can be found withing
the abstract of the article. For example one might interested in an article's
metadata for which the word eigenvalues is within the abstract.

For this example we are going to be using the API of Nature::

    >>> import arcas
    >>> api =  arcas.Nature()

Now all that is needed to specify in the parameters that we want `abstract='eigenvalues'`::

    >>> parameters = api.parameters_fix(title='eigenvalues')
    >>> url = api.create_url_search(parameters)

The query will be used to ping the API and afterwards we parse the response
that has been retrieved::

    >>> request = api.make_request(url)
    >>> root = api.get_root(request)
    >>> raw_article = api.parse(root)
    >>> article = api.to_dataframe(raw_article[0])

Note that Arcas can be used from the command line as well. To reproduce the query
in the command line would would type the following::

    $ arcas_scrape -p nature -a "eigenvalues"
