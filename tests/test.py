import os
import unittest
import dfquery
import json

PATH = os.path.dirname(os.path.abspath(__file__))


class DfQueryTest(unittest.TestCase):

    def test_str(self):
        abc = "*abc"

        index = abc.find('*')
        self.assertEqual(index, 0)


    def test_query(self):
        test_data = {}
        test_query = {}

        with open(os.path.join(PATH, 'data/test_data.json')) as f:
            test_data = json.load(f)
        with open(os.path.join(PATH, 'data/test_query.json')) as f:
            test_query = json.load(f)

        test_data = test_data.get('table_1')
        test_query = test_query.get('table_1')

        query = dfquery.make('table_1', test_data)
        query.query(test_query)
        results = query.build()

        self.assertEqual(results, {'table_1': {'name': ['abc']}})

    def test_queries(self):
        test_data = {}
        test_query = {}

        with open(os.path.join(PATH, 'data/test_data.json')) as f:
            test_data = json.load(f)
        with open(os.path.join(PATH, 'data/test_query.json')) as f:
            test_query = json.load(f)

        query = dfquery.batch(test_data)

        query.query(test_query)

        results = query.build()

        self.assertEqual(results, {'table_1': {'name': ['abc']}, 'table_2': {'name': ['abc']}})


if __name__ == '__main__':
    unittest.main()
