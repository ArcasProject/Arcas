[![Build
Status](https://travis-ci.org/Nikoleta-v3/Arcas.svg?branch=master)](https://travis-ci.org/Nikoleta-v3/Arcas)

# Arcas

Arcas is python tool designed to help with collecting academic articles
from various APIs.

## Installation

The easiest way to install is:

```bash
$ pip install arcas
```

## Usage

Arcas used docopt to pass a list of arguments.

For example:

```
$ arcas_scrape -p arxiv -t "Prisoner's Dilemma" -y 2000 -r 1
```
This query pings the arXiv api and ask for 1 record with title containing the 
words Prisoner's Dilemma and published year 2000. 


## Development

To install a development version of this library:

```
$ python setup.py develop
```

To run the full test suite:

```
$ python setup.py test
```