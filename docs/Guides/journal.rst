.. _journal:

How to: Collect articles' based on `journal`
==========================================

Articles can also be retrieved using the full journal name/publication title.

Thus sometime we might not be specifying only the publisher but the
exact journal as well. This can be done using the argument `journal`.

    >>> import arcas
    >>> api =  arcas.Nature()

Assume that we would like to fetch an article from Nature's Blood Cancer Journal.
The query message will be the following::

    >>> parameters = api.parameters_fix(journal='Blood Cancer Journal')
    >>> url = api.create_url_search(parameters)
    'http://www.nature.com/opensearch/request?&query=prism.publicationName=Blood Cancer Journal'
