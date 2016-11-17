"""IEEE Xplore API Request.

Usage:
    IEEE/main.py -h [-au AUTHOR] [-ti TITLE] [-ab ABSTRACT] [-py YEAR] [-hc
    NUMBER]

Options:
    -h --help               show this
    -au AUTHOR              Terms to search for in Author [default: ""]
    -ti TITLE               Terms to search for in Title [default: ""]
    -ab ABSTRACT            Terms to search for in the Abstract [default: ""]
    -py YEAR                Terms to search for in Year [default: ""]
    -hc NUMBER              Number of records to fetch. [default: 25]
"""

from scraping.tools import *
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='IEEE Xplore API Request')

parameters = [arguments['-au'], arguments['-ti'], arguments['-ab'],
              arguments['-py'], arguments['-hc']]

standard = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?'

url = create_url_search(parameters=parameters, standard=standard)
root = fetch_xml(url)

parents = root.getchildren()
[parents.remove(parents[0]) for _ in range(2)]

for document in parents:
    article = xml_to_dict(document)
    post = iee_to_axelbib(article)
    send = post_to_axelbib(post)
