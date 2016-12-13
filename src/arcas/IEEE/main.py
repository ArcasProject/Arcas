from arcas.tools import Api


class Ieee(Api):
    """
     API argument is 'ieee'.
    """
    def __init__(self):
        self.standard = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?'

    def to_json(self, article):
        """A function which takes a dictionary with structure of the IEEE
        results and transform it to a standardized format.
        """
        article['author'], article['key_word'], article['labels'], article[
            'list_strategies'] = [], [], [], []

        for i in article['authors'].split(';  '):
            article['author'].append({'name': i})

        for j in article['term'].split(','):
            article['key_word'].append({'key_word': j})

        article['date'] = {'year': int(article['py'])}
        article['journal'] = article.pop('pubtitle')
        article['pages'] = '{}-{}'.format(article['spage'], article['epage'])

        article['provenance'] = 'IEEE'
        article['read'] = False

        article['key'], article['unique_key'] = self.create_keys(article)

        post = {key: article[key] for key in self.keys()}

        return post

    def parse(self, root):
        """Removing unwanted branches."""
        try:
            parents = root.getchildren()
            articles = []
            for _ in range(2):
                parents.remove(parents[0])

            for record in parents:
                articles.append(self.xml_to_dict(record))
        except:
            articles = False

        return articles

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
        if arguments['-s'] is not None:
            parameters.append('rs={}'.format(arguments['-s']))

        return parameters
