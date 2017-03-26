import unittest
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.datetime import dates
from arcas.PLOS.main import Plos

plos_entry = st.fixed_dictionaries(
                   {'id': st.text(min_size=5, max_size=5),
                    'journal': st.text(min_size=5, max_size=5),
                    'article_type': st.text(min_size=5, max_size=5),
                    'author_display': st.lists(elements=st.text(min_size=5,
                                                                max_size=5),
                                               min_size=5, max_size=5,
                                               unique=True),
                    'abstract': st.text(min_size=5, max_size=5),
                    'title_display': st.text(min_size=5, max_size=5),
                    'score': st.text(min_size=5, max_size=5)
                    })

dummy_arguments = st.fixed_dictionaries(
                    {'-a': st.text(min_size=5, max_size=5),
                     '-t': st.text(min_size=5, max_size=5),
                     '-b': st.text(min_size=5, max_size=5),
                     '-y': st.text(min_size=5, max_size=5),
                     '-r': st.text(min_size=5, max_size=5),
                     '-s': st.text(min_size=5, max_size=5)
                     })

plos_keys = ['key', 'unique_key', 'title', 'author', 'abstract',
             'date', 'journal', 'provenance', 'score']


class TestArxiv(unittest.TestCase):

    def setUp(self):
        self.api = Plos()

    def test_keys(self):
        keys = self.api.keys()
        self.assertEqual(keys, plos_keys)

    @given(plos_entry)
    def test_to_dataframe(self, entry):

        a_date = dates(min_year=1000, max_year=2017).example()
        a_date = [str(a_date.year), str(a_date.month), str(a_date.day)]
        entry['publication_date'] = '-'.join(a_date)

        df = self.api.to_dataframe(entry)

        self.assertEqual(df['title'][0], entry['title_display'])
        self.assertEqual(list(df['author'].unique()), entry['author_display'])
        self.assertEqual(df['abstract'][0], entry['abstract'])
        self.assertEqual(df['date'][0], int(entry['publication_date'].split(
            '-')[0]))
        self.assertEqual(df['journal'][0], entry['journal'])
        self.assertEqual(df['provenance'][0], 'PLOS')

    @given(dummy_arguments)
    def test_parameters(self, arguments):
        parameters = self.api.parameters_fix(author=arguments['-a'], title=arguments['-t'],
                                             abstract=arguments['-b'],
                                             year=arguments['-y'],
                                             records=arguments['-r'],
                                             start=arguments['-s'])
        self.assertEqual('author:{}'.format(arguments['-a']), parameters[0])
        self.assertEqual('title:{}'.format(arguments['-t']), parameters[1])
        self.assertEqual('abstract:{}'.format(arguments['-b']), parameters[2])
        self.assertEqual('publication_date:[{0}-01-01T00:00:00Z TO '
                         '{0}-12-30T23:59:59Z]'.format(arguments['-y']),
                         parameters[3])
        self.assertEqual('rows={}'.format(arguments['-r']),
                         parameters[4])
        self.assertEqual(('start={}'.format(arguments['-s'])), parameters[5])
