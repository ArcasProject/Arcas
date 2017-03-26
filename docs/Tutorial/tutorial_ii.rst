.. _tutorial-ii:

===================================================
Tutorial II:  Retrieve an article from various APIs
===================================================

In this tutorial we are aiming to make a similar query, to that in
:ref:`tutorial I <tutorial-i>`, from different APIs.

To achieve that we will use a :code:`for` loop, to loop over a list of given
APIs classes. For each instance then repeat the following procedure::

    >>>  for p in [arcas.Ieee, arcas.Plos, arcas.Arxiv, arcas.Springer, arcas.Nature]:

    ...      api = p()
    ...      parameters = api.parameters_fix(title='Game', abstract='Game', records=1)
    ...      url = api.create_url_search(parameters)
    ...      request = api.make_request(url)
    ...      root = api.get_root(request)
    ...      raw_article = api.parse(root)

    ...      for art in raw_article:
    ...          article = api.to_dataframe(art)
    ...          api.export(article, 'results_{}.json'.format(api.__class__.__name__))


The :code:`export` function, is a function that writes the results to a `json
<http://www.json.org/>`_ file. Here the results of each API are stored to
a different file named after which API they come from.