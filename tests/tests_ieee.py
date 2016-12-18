import unittest
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.datetime import dates
from arcas.IEEE.main import Ieee

ieee_entry = st.fixed_dictionaries(
                  {'title': st.text(min_size=5, max_size=5),
                   'authors': st.lists(elements=st.text(min_size=5,
                                                        max_size=5),
                                       min_size=5, max_size=5, unique=True),
                   'affiliations': st.text(min_size=5, max_size=5),
                   'term': st.lists(elements=st.text(min_size=5,max_size=5),
                                    min_size=5, max_size=5),
                   'pubtitle': st.text(min_size=5, max_size=5),
                   'punumber': st.text(min_size=5, max_size=5),
                   'spage': st.text(max_size=3),
                   'epage': st.text(max_size=3),
                   'publisher': st.text(min_size=5, max_size=5),
                   'py': dates(min_year=1000, max_year=2010),
                   'abstract': st.text(min_size=5, max_size=5),
                   'issn': st.text(min_size=5, max_size=5),
                   'doi': st.text(min_size=5, max_size=5),
                   'publicationId': st.text(min_size=5, max_size=5),
                   'partnum': st.text(min_size=5, max_size=5),
                   'mdurl': st.text(min_size=5, max_size=5),
                   'pdf': st.text(min_size=5, max_size=5)})

dummy_arguments = st.fixed_dictionaries(
                    {'-a': st.text(min_size=5, max_size=5),
                     '-t': st.text(min_size=5, max_size=5),
                     '-b': st.text(min_size=5, max_size=5),
                     '-y': st.text(min_size=5, max_size=5),
                     '-r': st.text(min_size=5, max_size=5),
                     '-s': st.text(min_size=5, max_size=5)
                     })

ieee_keys = ['key', 'unique_key', 'title', 'author', 'abstract',
             'date', 'journal', 'pages', 'key_word', 'provenance']


class TestIEEE(unittest.TestCase):
    def setUp(self):
        self.api = Ieee()

    def test_keys(self):
        keys = self.api.keys()
        self.assertEqual(keys, ieee_keys)

    @given(ieee_entry)
    def test_to_dataframe(self, entry):

        entry['py'] = str(entry['py'].year)
        entry['authors'] = '; '.join(entry['authors'])
        entry['term'] = '_ '.join(entry['term'])

        df = self.api.to_dataframe(entry)

        self.assertEqual(df['title'][0], entry['title'])
        self.assertEqual(list(df['author'].unique()),  entry[
            'authors'].split('; '))
        self.assertEqual(df['abstract'][0], entry['abstract'])
        self.assertEqual(df['date'][0], int(entry['py'].split('-')[0]))
        self.assertEqual(df['journal'][0], entry['pubtitle'])
        self.assertEqual(df['pages'][0], '{}-{}'.format(entry['spage'],
                                                        entry['epage']))
        self.assertEqual(df['provenance'][0], 'IEEE')

        self.assertEqual(list(df['key_word'].unique()), entry['term'].split(
            ','))

    @given(dummy_arguments)
    def test_parameters(self, arguments):
        parameters = self.api.parameters_fix(arguments)
        self.assertEqual('au={}'.format(arguments['-a']), parameters[0])
        self.assertEqual('ti={}'.format(arguments['-t']), parameters[1])
        self.assertEqual('ab={}'.format(arguments['-b']), parameters[2])
        self.assertEqual('py={}'.format(arguments['-y']), parameters[3])
        self.assertEqual('hc={}'.format(arguments['-r']),
                         parameters[4])
        self.assertEqual(('rs={}'.format(arguments['-s'])), parameters[5])
