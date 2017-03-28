[![Build
Status](https://travis-ci.org/Nikoleta-v3/Arcas.svg?branch=master)](https://travis-ci.org/Nikoleta-v3/Arcas)

# Arcas

Arcas is a python tool designed to help with collecting academic articles
from various APIs.

## Installation

The easiest way to install it is:

```bash
$ pip install arcas
```

## Usage

Arcas uses `docopt` to pass a list of arguments.

For example:

```
$ arcas_scrape -p arxiv -t "Prisoner's Dilemma" -y 2000 -r 1
```

This query pings the arXiv api and asks for 1 record with the title containing
the words Prisoner's Dilemma and published year 2000.


## Development

To install a development version of this library:

```
$ python setup.py develop
```

To run the full test suite:

```
$ python setup.py test
```
