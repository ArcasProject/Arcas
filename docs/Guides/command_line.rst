.. _command_line:

How to use Arcas from the command line
======================================

Arcas is a tool which can be used by the command line as well. Arcas uses a package
called :code:docopt for passing arguments via the command line.

To get information on the arguments we can pass we type the following command
in a command prompt window::

    $ arcas_scrape --h 
    Arcas. A library to facilitate scraping of APIs for scholarly resources.

    Usage:
        arcas_scrape  [-h] [-p API] [-a AUTHOR] [-t TITLE] [-b ABSTRACT] [-y YEAR]
                    [-r RECORDS] [-s START] [-v VALIDATE] [-f FILENAME]
        arcas_scrape --version


    Options:
        -h --help              Show this
        --version              Show version.
        -p API                 The online API, from a given list, to parse [default: arxiv]
        -a AUTHOR              Terms to search for in Author
        -t TITLE               Terms to search for in Title
        -b ABSTRACT            Terms to search for in the Abstract
        -y YEAR                Terms to search for in Year
        -r RECORDS             Number of records to fetch [default: 1]
        -s START               Sequence number of first record to fetch [default: 1]
        -v VALIDATE            Checks if query returned with arguments asked [default: False]
        -f FILENAME            Name of json file [default: results.json]
