from arcas.tools import Api
from xml.etree import ElementTree


class Arxiv(Api):
    """
     API argument is 'ieee'.
    """
    def __init__(self):
        self.standard = 'http://export.arxiv.org/api/query?search_query='

    def to_json(self, article):
        """A function which takes a dictionary with structure of the arXiv
        results and transform it to a standardized format.
        """
        article = {k.split('}')[-1]: v for k, v in article.items()}
        article['author'] = article.get('name', None)
        article['key_word'] = article.get('primary_category', None)

        if article['author'] is not None:
            article['author'] = [{'name': author} for author in article[
                'author'].split(',')]
        else:
            article['author'] = [{'name': str(None)}]

        if article['key_word'] is not None:
            article['key_word'] = [{'key_word': word} for word in
                                   article['primary_category']]
        else:
            article['key_word'] = [{'key_word': str(None)}]

        article['date'] = {'year': int(article.get('published', '0').split('-')[
                                                       0])}

        article['journal'] = article.get('journal_ref', None)
        if article['journal'] is None:
            article['journal'] = "arXiv"

        article['abstract'] = article.get('summary', None)
        article['title'] = article.get('title', None)
        article['pages'] = " "
        article['provenance'] = 'arXiv'
        article['read'] = False

        article['key'], article['unique_key'] = self.create_keys(article)

        post = {key: article[key] for key in self.keys()}

        return post

    def parse(self, root):
        """Removing unwanted branches."""
        parents = root.getchildren()
        articles = []
        for _ in range(7):
            parents.remove(parents[0])
        if not parents:
            articles = False
        else:
            for record in parents:
                articles.append(self.xml_to_dict(record))
        return articles

    @staticmethod
    def parameters_fix(arguments):
        parameters = []
        if arguments['-a'] is not None:
            parameters.append('au:{}'.format(arguments['-a']))
        if arguments['-t'] is not None:
            parameters.append('ti:{}'.format(arguments['-t']))
        if arguments['-b'] is not None:
            parameters.append('abs:{}'.format(arguments['-b']))
        if arguments['-r'] is not None:
            parameters.append('max_results={}'.format(arguments['-r']))
        if arguments['-s'] is not None:
            parameters.append('start={}'.format(arguments['-s']))

        return parameters

    @staticmethod
    def get_root(response):
        root = ElementTree.fromstring(response.text)
        return root
