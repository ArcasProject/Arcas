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
        article['author'] = article.get('authors', None)
        article['key_word'] = article.get('term', None)

        if article['author'] is not None:
            article['author'] = [{'name': author} for author in article[
                'author'].split('; ')]
        else:
            article['author'] = [{'name': str(None)}]

        if article['key_word'] is not None:
            article['key_word'] = [{'key_word': word} for word in article[
                                                         'key_word'].split(',')]
        else:
            article['key_word'] = [{'key_word': str(None)}]

        article['date'] = {'year': int(article.get('py', '0'))}
        article['journal'] = article.get('pubtitle', 'None')
        article['pages'] = '{}-{}'.format(article.get('spage', 'None'),
                                          article.get('epage', 'None'))
        article['abstract'] = article.get('abstract', 'None')
        article['title'] = article.get('title', 'None')

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
