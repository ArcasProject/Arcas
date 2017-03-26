import unittest
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.datetime import dates
from arcas.Springer.main import Springer
import string

springer_entry = st.fixed_dictionaries({
                    'records': st.text(min_size=5, max_size=5),
                    'message': st.text(min_size=5, max_size=5),
                    'head': st.text(min_size=5,max_size=5),
                    'article': st.text(min_size=5, max_size=5),
                    'identifier': st.text(min_size=5, max_size=5),
                    'title': st.text(min_size=5, max_size=5),
                    'creator': st.lists(st.text(min_size=5, max_size=5, alphabet=string.ascii_lowercase),
                                                 min_size=5, max_size=5,
                                        unique=True),
                    'publicationName': st.text(min_size=5,
                                                        max_size=5),
                    'printIsbn': st.text(min_size=5, max_size=5),
                    'electronicIsbn': st.text(min_size=5, max_size=5),
                    'publisher': st.text(min_size=5, max_size=5),
                    'body': st.text(min_size=5, max_size=5),
                    'h1': st.text(min_size=5, max_size=5),
                    'p': st.text(min_size=5, max_size=5)})

dummy_arguments = st.fixed_dictionaries(
                    {'-a': st.text(min_size=5, max_size=5),
                     '-t': st.text(min_size=5, max_size=5),
                     '-b': st.text(min_size=5, max_size=5),
                     '-y': st.text(min_size=5, max_size=5),
                     '-r': st.text(min_size=5, max_size=5),
                     '-s': st.text(min_size=5, max_size=5)
                     })

springer_keys = ['key', 'unique_key', 'title', 'author', 'abstract',
                 'date', 'journal', 'provenance']


class TestSpinger(unittest.TestCase):
    def setUp(self):
        self.api = Springer()

    def test_keys(self):
        keys = self.api.keys()
        self.assertEqual(keys, springer_keys)

    @given(springer_entry)
    def test_to_json(self, entry):

        a_date = dates(min_year=1000, max_year=2017).example()
        a_date = [str(a_date.year), str(a_date.month), str(a_date.day)]
        entry['publicationDate'] = '-'.join(a_date)
        entry['creator'] = ';'.join(entry['creator'])

        df = self.api.to_dataframe(entry)

        self.assertEqual(df['title'][0], entry['title'])
        self.assertEqual(list(df['author'].unique()), entry['creator'].split(
            ','))
        self.assertEqual(df['abstract'][0], entry['p'])
        self.assertEqual(df['date'][0], int(entry['publicationDate'].split('-')[0]))
        self.assertEqual(df['journal'][0], entry['publicationName'])
        self.assertEqual(df['provenance'][0], 'Springer')

    @given(dummy_arguments)
    def test_parameters(self, arguments):
        parameters = self.api.parameters_fix(author=arguments['-a'], title=arguments['-t'],
                                             abstract=arguments['-b'],
                                             year=arguments['-y'],
                                             records=arguments['-r'],
                                             start=arguments['-s'])
        self.assertEqual('name:{}'.format(arguments['-a']), parameters[0])
        self.assertEqual('title:{}'.format(arguments['-t']),
                         parameters[1])
        self.assertEqual('year:{}'.format(arguments['-y']),
                         parameters[2])
        self.assertEqual('p={}'.format(arguments['-r']),
                         parameters[3])
        self.assertEqual(('s={}'.format(arguments['-s'])),
                         parameters[4])
