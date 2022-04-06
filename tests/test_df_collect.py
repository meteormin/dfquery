import dfquery

test_data = {
    "test_1": [
        {
            "id": 1,
            "name": "abc",
        },
        {
            "id": 2,
            "name": "4939"
        }
    ],
    "test_2": [
        {
            "id": 1,
            "name": "abc",
            "cols": 3
        },
        {
            "id": 2,
            "name": "4939",
            "cols": 1010
        }
    ]
}

query = dfquery.batch(test_data)

query.query({
    "test_1": {
        "test_name": {
            "select": ["name"],
            "where": [
                {
                    "key": "id",
                    "operator": "==",
                    "value": 1
                }
            ]
        }
    },
    "test_2": {
        "test_name": {
            "select": ["name"],
            "where": [
                {
                    "key": "id",
                    "operator": "==",
                    "value": 1
                }
            ]
        }
    }
})

print(query.build())
