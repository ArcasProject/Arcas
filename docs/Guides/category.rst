.. _category:

How to: Collect articles' based on `category`
============================================

Subject terms are often given to articles either by the authors or the journals
themselves. Arcas allow the user to search articles that satisfies a given subject
term using the :code:`category` argument.

For example the query for a game theoretic article in arXiv would be the following::

    >>> import arcas
    >>> api =  arcas.Nature()
    >>> parameters = api.parameters_fix(category='Game Theory')
    >>> url = api.create_url_search(parameters)
    'http://www.nature.com/opensearch/request?&query=dc.subject adj Game Theory'
