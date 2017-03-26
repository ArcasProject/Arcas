.. _tutorial-iii:

====================================================
Tutorial III:  Retrieving a large number of articles
====================================================

Now that we have learned to ping several APIs for a single article, we will
repeat the procedure for a large number of articles. In this example the
number of articles we would like to retrieve is 20 from each API.

Often, we are looking for hundreds of articles. Rather than asking the API
for all the results at once, the APIs offer a paging mechanism through
:code:`start` and :code:`records`. That way we can receive chunks of the
result set at a time. :code:`start` defines the index of the first returned
article and :code:`records` the number of articles returned by the query.

    >>> for p in [arcas.Ieee, arcas.Plos, arcas.Arxiv, arcas.Springer, arcas.Nature]:
    ...    for start in range(2):
    ...
    ...        api = p()
    ...        parameters = api.parameters_fix(title='Game', abstract='Game',
    ...                                        records=10, start=(start * 10))
    ...        url = api.create_url_search(parameters)
    ...        request = api.make_request(url)
    ...        root = api.get_root(request)
    ...        raw_article = api.parse(root)
    ...
    ...    for art in raw_article:
    ...        article = api.to_dataframe(art)
    ...        api.export(article, 'results_{}.json'.format(api.__class__.__name__))

In our example this might not seem as an important difference. But assume you
were asking for a hundred of articles. Some APIs have a limited number of
articles that be can returned, thus using this practice we avoid overloading
the API.