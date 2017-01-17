import unittest
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.datetime import dates
from arcas.arXiv.main import Arxiv

arxiv_entry = st.fixed_dictionaries(
                   {'{http://}affiliation': st.text(min_size=5, max_size=5),
                    '{http://}author': st.text(min_size=5, max_size=5),
                    '{http://}category': st.booleans(),
                    '{http://}comment': st.text(min_size=5, max_size=5),
                    '{http://}doi': st.text(min_size=5, max_size=5),
                    '{http://}entry': st.text(min_size=5, max_size=5),
                    '{http://}id': st.text(min_size=5, max_size=5),
                    '{http://}journal_ref': st.text(min_size=5, max_size=5),
                    '{http://}link': st.booleans(),
                    '{http://}name': st.lists(elements=st.text(min_size=5,
                                                               max_size=5),
                                              min_size=5, max_size=5,
                                              unique=True),
                    '{http://}primary_category': st.text(min_size=5,
                                                         max_size=5),
                    '{http://}summary': st.text(min_size=5, max_size=5),
                    '{http://}title': st.text(min_size=5, max_size=5),
                    '{http://}updated': st.text(min_size=5, max_size=5),
                    })

dummy_arguments = st.fixed_dictionaries(
                    {'-a': st.text(min_size=5, max_size=5),
                     '-t': st.text(min_size=5, max_size=5),
                     '-b': st.text(min_size=5, max_size=5),
                     '-r': st.text(min_size=5, max_size=5),
                     '-s': st.text(min_size=5, max_size=5)
                     })

arxiv_keys = ['key', 'unique_key', 'title', 'author', 'abstract',
              'date', 'journal', 'provenance']


class TestArxiv(unittest.TestCase):

    def setUp(self):
        self.api = Arxiv()

    def test_keys(self):
        keys = self.api.keys()
        self.assertEqual(keys, arxiv_keys)

    @given(arxiv_entry)
    def test_to_json(self, entry):

        a_date = dates(min_year=1000, max_year=2017).example()
        a_date = [str(a_date.year), str(a_date.month), str(a_date.day)]
        entry['{http://}published'] = '-'.join(a_date)
        entry['{http://}name'] = ','.join(entry['{http://}name'])

        df = self.api.to_dataframe(entry)

        self.assertEqual(df['title'][0], entry['{http://}title'])
        self.assertEqual(list(df['author']), entry['{http://}name'].split(','))
        self.assertEqual(df['abstract'][0], entry['{http://}summary'])
        self.assertEqual(df['date'][0], int(entry['{http://}published'].split('-')[0]))
        self.assertEqual(df['journal'][0], entry['{http://}journal_ref'])
        self.assertEqual(df['provenance'][0], 'arXiv')

    @given(dummy_arguments)
    def test_parameters(self, arguments):
        parameters = self.api.parameters_fix(arguments)
        self.assertEqual('au:{}'.format(arguments['-a']), parameters[0])
        self.assertEqual('ti:{}'.format(arguments['-t']), parameters[1])
        self.assertEqual('abs:{}'.format(arguments['-b']), parameters[2])
        self.assertEqual('max_results={}'.format(arguments['-r']),
                         parameters[3])
        self.assertEqual(('start={}'.format(arguments['-s'])), parameters[4])
