import unittest
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.datetime import dates
from arcas.nature.main import Nature
import string

nature_entry = st.fixed_dictionaries({
                     'message': st.text(min_size=5, max_size=5),
                     'article': st.text(min_size=5, max_size=5),
                     'head': st.text(min_size=5, max_size=5),
                     'identifier': st.text(min_size=5, max_size=5),
                     'title': st.text(min_size=5, max_size=5),
                     'creator': st.lists(st.text(min_size=5,
                                                 max_size=5, alphabet=string.ascii_lowercase),
                                        min_size=5, max_size=5,
                                         unique=True, ),
                     'publicationName': st.text(min_size=5, max_size=10),
                     'eIssn': st.text(min_size=5, max_size=5),
                     'doi': st.text(min_size=5, max_size=5),
                     'publisher': st.text(min_size=5, max_size=5),
                     'subject': st.lists(st.text(min_size=5,
                                                 max_size=5, alphabet=string.ascii_lowercase),
                                         min_size=5, max_size=5, unique=True),
                     'description': st.text(min_size=5, max_size=5)
})

dummy_arguments = st.fixed_dictionaries(
                    {'-a': st.text(min_size=5, max_size=5),
                     '-t': st.text(min_size=5, max_size=5),
                     '-b': st.text(min_size=5, max_size=5),
                     '-y': st.text(min_size=5, max_size=5),
                     '-r': st.text(min_size=5, max_size=5),
                     '-s': st.text(min_size=5, max_size=5)
                     })

nature_keys = ['key', 'unique_key', 'title', 'author', 'abstract',
               'date', 'journal', 'key_word', 'provenance']


class TestNature(unittest.TestCase):
    def setUp(self):
        self.api = Nature()

    def test_keys(self):
        keys = self.api.keys()
        self.assertEqual(keys, nature_keys)

    @given(nature_entry)
    def test_to_json(self, entry):

        a_date = dates(min_year=1000, max_year=2017).example()
        a_date = [str(a_date.year), str(a_date.month), str(a_date.day)]
        entry['publicationDate'] = '-'.join(a_date)
        entry['creator'] = ','.join(entry['creator'])
        entry['subject'] = ','.join(entry['subject'])

        df = self.api.to_dataframe(entry)

        self.assertEqual(df['title'][0], entry['title'])
        self.assertEqual(list(df['author'].unique()),  entry['creator'].split(','))
        self.assertEqual(df['abstract'][0], entry['description'])
        self.assertEqual(df['date'][0], int(entry['publicationDate'].split('-')[0]))
        self.assertEqual(list(df['key_word'].unique()), entry['subject'].split(
                                                                            ','))
        self.assertEqual(df['journal'][0], entry['publisher'])
        self.assertEqual(df['provenance'][0], 'Nature')

    @given(dummy_arguments)
    def test_parameters(self, arguments):
        parameters = self.api.parameters_fix(author=arguments['-a'], title=arguments['-t'],
                                             abstract=arguments['-b'],
                                             year=arguments['-y'],
                                             records=arguments['-r'],
                                             start=arguments['-s'])
        self.assertEqual('dc.creator={}'.format(arguments['-a']), parameters[0])
        self.assertEqual('dc.title adj {}'.format(arguments['-t']),
                         parameters[1])
        self.assertEqual('dc.description adj {}'.format(arguments['-b']),
                         parameters[2])
        self.assertEqual('prism.publicationDate={}'.format(arguments['-y']),
                         parameters[3])
        self.assertEqual('maximumRecords={}'.format(arguments['-r']),
                         parameters[4])
        self.assertEqual(('startRecord={}'.format(arguments['-s'])),
                         parameters[5])




