.. _title:

How to: Collect articles' based on `title`
==========================================

Academic articles are published with a given title by their authors. Some times
we found ourselves in search of articles relevant to our field and we do not
know where to start. The most common approach is to search articles where a word
describing our topic of interest is included in the article's title.

For example a mathematician might be interested in looking for articles' that
the world eigenvalues appears on the title.

Initially we need to chose a publisher, for this example we assume that
we are interested in the articles published by Nature::

    >>> import arcas
    >>> api =  arcas.Nature()

Now all that is needed to specify in the parameters that we want `title='eigenvalues'`::

    >>> parameters = api.parameters_fix(title='eigenvalues')
    >>> url = api.create_url_search(parameters)

The query will be used to ping the API and afterwards we parse the response
that has been retrieved::

    >>> request = api.make_request(url)
    >>> root = api.get_root(request)
    >>> raw_article = api.parse(root)
    >>> article = api.to_dataframe(raw_article[0])

We can perform an insanity check and reassure that :code:`'eigenvalues'` is indeed
within the title:

    >>> 'eigenvalues' in article['title'].unique()[0]
    True

Note that Arcas can be used from the command line as well. If we wanted to
reproduced the same example the command would be::

    $ arcas_scrape -p nature -t "eigenvalues"
