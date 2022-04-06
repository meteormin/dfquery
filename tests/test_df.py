import dfquery

test_data = [
    {
        "id": 1,
        "name": "abc",
    },
    {
        "id": 2,
        "name": "4939"
    }
]

core = dfquery.make('tests', test_data)

core.query({
    "test_1": {
        "select": ["name"],
        "where": [
            {
                "key": "id",
                "operator": "==",
                "value": 1
            }
        ]
    }
})

print(core.build())
