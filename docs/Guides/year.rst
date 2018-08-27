.. _year:

How to: Collect articles' based on `year`
=========================================

Publication date of an article is another search field available with Arcas.
Consider an example whereas we are interested in articles that have been published
on a specific year.

Let us assume that we are interested in the first article that will is returned
by Plos that has been publish in 1993::

    >>> import arcas
    >>> api =  arcas.Plos()

Now all that is needed to specify in the parameters that we want `year=1993`::

    >>> parameters = api.parameters_fix(year=1993)
    >>> url = api.create_url_search(parameters)

The url can be used to retrieve the response which is then passed to a data
frame::

    >>> request = api.make_request(url)
    >>> root = api.get_root(request)
    >>> raw_article = api.parse(root)
    >>> article = api.to_dataframe(raw_article[0])

The same example can be used to collect the article using the command line::
   
    $ arcas_scrape -p plos -y 1993
