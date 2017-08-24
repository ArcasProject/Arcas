[![Build
Status](https://travis-ci.org/Nikoleta-v3/Arcas.svg?branch=master)](https://travis-ci.org/Nikoleta-v3/Arcas)

# Arcas

Arcas is a python tool designed to help with collecting academic articles
from various APIs.

Features
--------

Arcas allows you:

- access meta data from different academic APIs.
- a collection of examples of analysing such meta data.

Installation
-------------

The easiest way to install it is:

```
$ pip install arcas
```

To install from source::

```
$ git clone https://github.com/Nikoleta-v3/Arcas.git
$ cd Arcas
$ python setup.py install
```

Usage
-----

Arcas uses `docopt` to pass a list of arguments.

For example:

```
$ arcas_scrape -p arxiv -t "Prisoner's Dilemma" -y 2000 -r 1
```

This query pings the arXiv api and asks for 1 record with the title containing
the words Prisoner's Dilemma and published year 2000.

Documentation
-------------
The full documentation can be found here: http://arcas.readthedocs.io/en/latest/index.html.


Examples
--------

A repository that contains a set of example: https://github.com/ArcasProject/ArcasExamples


Contribution
------------

All contributions are welcome!
