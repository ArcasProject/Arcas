from scraping.tools import Api


class Ieee(Api):
    """
     API argument is 'ieee'.
    """
    def __init__(self):
        self.standard = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?'

    @staticmethod
    def to_axelbib(article):
        """A function which takes a dictionary with structure of the IEEE results
        and transform it to a structure understandable by Axelbib"""
        keys = ['key', 'title', 'abstract', 'author', 'date', 'journal',
                'pages', 'labels', 'list_strategies']

        article['author'] = []
        for i in article['authors'].split(';  '):
            article['author'].append({'name': i})
        article['date'] = {'year': int(article['py'])}
        article['journal'] = article.pop('pubtitle')

        full_name = article['author'][0]['name'].split(' ')
        print(full_name)
        year = article['date']['year']
        print(full_name[-1])
        article['key'] = '{}{}'.format(full_name[-1], year)
        article['pages'], article['labels'], article['list_strategies'] = "", [], []

        post = {key: article[key] for key in keys}

        return post

    @staticmethod
    def parse(root):
        """Removing unwanted branches."""
        parents = root.getchildren()
        for _ in range(2):
            parents.remove(parents[0])
        return parents

    @staticmethod
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('au={}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('ti={}'.format(arguments['-t']))
        if arguments['-b'] is not None:
            parameters.append('ab={}'.format(arguments['-b']))
        if arguments['-y'] is not None:
            parameters.append('py={}'.format(arguments['-y']))
        if arguments['-r'] is not None:
            parameters.append('hc={}'.format(arguments['-r']))

        return parameters



