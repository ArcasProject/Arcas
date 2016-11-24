"""API Request.

Usage:
    scrape.py [-h] [-p API] [-a AUTHOR] [-t TITLE] [-b ABSTRACT] [-y YEAR]
              [-r RECORDS]

Options:
    -h --help              show this
    -p API                 The online API , from a given list, to parse [default: "ieee"]
    -a AUTHOR              Terms to search for in Author
    -t TITLE               Terms to search for in Title
    -b ABSTRACT            Terms to search for in the Abstract
    -y YEAR                Terms to search for in Year
    -r RECORDS             Number of records to fetch
"""

from scraping import *
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='API Request')

    apis = {"ieee": Ieee, "arxiv": Arxiv}
    api = apis[arguments['-p']]()

    parameters = api.parameters_fix(arguments)
    print(parameters)
    api.run(parameters)
