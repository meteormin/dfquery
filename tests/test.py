import os
import unittest
import dfquery
import json

PATH = os.path.dirname(os.path.abspath(__file__))


class DfQueryTest(unittest.TestCase):

    @staticmethod
    def get_data():
        with open(os.path.join(PATH, 'data/test_data.json')) as f:
            test_data = json.load(f)
        with open(os.path.join(PATH, 'data/test_query.json')) as f:
            test_query = json.load(f)
        return {
            'data': test_data,
            'query': test_query
        }

    def test_query(self):
        test_data, test_query = self.get_data().values()

        test_data = test_data.get('table_1')
        test_query = test_query.get('table_1')

        query = dfquery.make('table_1', test_data)
        query.query(test_query)
        results = query.build()

        self.assertEqual(results, {'table_1': {'name': ['aabc']}})

    def test_queries(self):
        test_data, test_query = self.get_data().values()

        query = dfquery.batch(test_data)

        query.query(test_query)

        results = query.build()

        self.assertEqual(results, {'table_1': {'name': ['aabc']}, 'table_2': {'name': ['abcdefg']}})

    def test_table(self):
        test_data, test_query = self.get_data().values()
        table_name = 'table_1'
        query = dfquery.make(table_name, test_data.get('table_1'))

        tbl = dfquery.table(table_name)
        gen = tbl.name('table_test').select('name').where({
            "key": "name",
            "operator": "like",
            "value": "*abc"
        })

        query.query(gen)
        results = query.build()

        self.assertEqual(results, {'table_1': {'name': ['aabc']}, 'table_2': {'name': ['abcdefg']}})

    def test_tables(self):
        test_data, test_query = self.get_data().values()
        tables = dfquery.tables()
        for name, query in test_query.items():
            tbl = dfquery.table(name)
            for n, q in query.items():
                tbl.name(n).select(q['select']).where(q['where'])

            tables.append(tbl)

        self.assertEqual(tables.to_dict(), test_query)


if __name__ == '__main__':
    unittest.main()
