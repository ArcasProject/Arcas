.. _results-set:

Results set
===========

Each response of the API returns a list of metadata for a given article.
This list differs for each API. Arcas is designed to return a similar set of
metadata for any given API. Thus the json results of Arcas has the following
list of metadata:

- :code:`key`
    - A generated key containing an authors name and publication year (e.g. Glynatsi2017)
- :code:`unique_key`
    - A unique key generated using the `hashlib <https://docs.python.org/2/library/hashlib.html>`_
      python library. The hashable string is created by: [author name, title,
      year,abstract]
- :code:`title`
    - Title of article
- :code:`author`
    - A single entity of an author from the list of authors of the respective article
- :code:`abstract`
    - The abstract of the article
- :code:`date`
    - Date of publication
- :code:`journal`
    - Journal of publication
- :code:`pages`
    - Pages of publication
- :code:`key_word`
    -  A single entity of a keyword assigned to the article by the given journal
- :code:`provenance`
    - Scholarly database for where the article was collected
- :code:`score`
    - Score given to article by the given journal