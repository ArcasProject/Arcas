.. _search-fields:

Search Parameters
=============

The table below outlines the parameters that can be passed to the query interface:


+-----------------+----------------------------------------------------------------------------------------------+
| Parameter       | Description                                                                                  |
+=================+==============================================================================================+
| :code:`author`  | Searches both first name and last name.                                                      |
+-----------------+----------------------------------------------------------------------------------------------+
| :code:`title`   | Locate documents containing a word or phrase in the "article title" element.                 |
+-----------------+----------------------------------------------------------------------------------------------+
| :code:`abstract`| Locate documents containing a word or phrase in the "abstract" element.                      |
+-----------------+----------------------------------------------------------------------------------------------+
| :code:`year`    | The value for publication year.                                                              |
+-----------------+----------------------------------------------------------------------------------------------+
| :code:`category`| Allows users to search the by keywords given to an article.                                  |
+-----------------+----------------------------------------------------------------------------------------------+
| :code:`journal` | Locate documents containing a word or phrase in the "full journal/publication title" element.|
+-----------------+----------------------------------------------------------------------------------------------+
| :code:`records` | The number of records to fetch.                                                              |
+-----------------+----------------------------------------------------------------------------------------------+
| :code:`start`   | Sequence number of first record to fetch.                                                    |
+-----------------+----------------------------------------------------------------------------------------------+

If a search argument is not available for a given API a message will be displayed.