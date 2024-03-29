# DfQuery
<img alt="Version" src="https://img.shields.io/badge/version-v1.0.1-blue.svg?cacheSeconds=2592000" />
<img src="https://img.shields.io/badge/Python3.8-3776AB?logo=python&logoColor=white" />

Pandas DataFrame 조회를 양식화된 JSON(내부에선 딕셔너리 객체)으로 원하는 값을 가져올 수 있습니다.

## 목적

Pandas DataFrame 조회를 별도의 코드 수정없이 JSON과 같이 ```name: value``` 형태의 자료구조를 활용하여 원하는 값을 조회하고자 했습니다.

Python에서 딕셔너리로 변환 가능한 자료구조는 모두 가능 합니다.

## 사용법

### 설치

```
git clone https://github.com/miniyus/dfquery
cd dfquery
python setup.py install
```

### 기본 예시

```python
import dfquery
import json

# single table
file = open('table_file_path')
json_dict = json.load(file)
query = dfquery.make('table_name', json_dict)

query_dict = json.load(open('query_file_path'))
query.query(query_dict)
print(query.build())

# multiple table
file = open('table_file_path')
json_dict = json.load(file)
query = dfquery.batch(json_dict)

query_dict = json.load(open('query_file_path'))
query.query(query_dict)
print(query.build())
```

### dfquery.make()

```python
import pandas
import dfquery

"""
data: 데이터 프레임으로 변환 가능한 객체
"""
data = pandas.DataFrame()
dfquery.make('table_name', data)

"""
data: 딕셔너리의 경우, 데이터 프레임의 from_dict 메서드를 사용하기 때문에
orient 파라미터가 존재합니다. 딕셔너리 구조에 맞게 사용하세요.
"""
data = {}
dfquery.make('table_name', data)

"""
data: list[dict] 형태의 records 형식은 from_records 메서드를 사용하여 dataframe으로 변환합니다.
"""
data = [{}]
dfquery.make('table_name', data)

```

### dfquery.batch()

```python
import dfquery

"""
make에서 사용된 구조와 동일한 형식의 데이터들이 딕셔너리로 감싸진 형태

{
  "table_1" : data(Type: DataFrame, list[dict], dict),
  "table_2" : data(Type: DataFrame, list[dict], dict)
}

딕셔너리의 경우 make와 동일하게 orient 파라미터가 존재하지만, 모든 테이블이 같은 구조일경우만 정상 작동합니다.
"""
batch_data = {}
query = dfquery.batch({
    "table_1": [{...}],
    "table_2": [{...}]
})

```

### 쿼리 구조

```json
{
  "table_name": {
    "name(결과를 찾을 때 사용)": {
      "select": [
        "column_name"
      ],
      "where": [
        {
          "key": "column_name",
          "operator": "파이썬 비교 연산자",
          "value": "find_value"
        }
      ]
    },
    "name2": {
      "select": [
        "column_name"
      ],
      "where": [
        {
          "key": "column_name",
          "operator": "파이썬 비교 연산자",
          "value": "find_value"
        }
      ]
    }
  }
}
```

**문법**

- select: 가져올 컬럼명 리스트
    - ```"*"```를 입력한 경우, 모든 컬럼을 가져오며, ```"*"```의 순서와 상관 없이 select 리스트에 포함 되어 있는 경우 모든 컬럼을 조회합니다.
- where:
    - key: 조건에 사용할 컬럼명
        - operator: 비교 조건, python에서 사용하는 기본 비교 연산자 사용 가능
            - *like: 와일드카드```"*"```를 사용(SQL like와 유사하다.)
                - ```"*ABC*"```: ABC가 포함된 값 찾기
                - ```"*ABC"```: ABC(으)로 끝나는 값 찾기
                - ```"ABC*"```: ABC(으)로 시작하는 값 찾기
          ```json
          {
            "key": "column_name",
            "operator": "like",
            "value": "*ABC*"    
          }
          ```
    - where절도 리스트이기 때문에 여러개의 조건을 포함할 수 있으나 OR 조건처럼 작동한다.

### dfquery.table()

딕셔너리가 아닌 런타임 코드 작성

```python
import dfquery
import json

# Generator 객체로 넘기기
table_name = 'table_1'
file = open('table_file_path')
json_dict = json.load(file)

query = dfquery.make(table_name, json_dict.get('table_1'))

tbl = dfquery.table(table_name)
gen = tbl.name('table_test').select('name').where({
    "key": "name",
    "operator": "like",
    "value": "*abc"
})

query.query(gen)
results = query.build()
print(results)

# Table 객체로 넘기는 방법
table_name = 'table_1'
file = open('table_file_path')
json_dict = json.load(file)
query = dfquery.batch(json_dict)

tbl = dfquery.table(table_name)
tbl.name('table_test').select('name').where({
    "key": "name",
    "operator": "like",
    "value": "*abc"
})

query.query(tbl)
results = query.build()
print(results)
```

### dfquery.tables()

여러개의 테이블을 사용할 경우 런타임 코드 작성

```python
import dfquery
import json

# Generator 객체로 넘기기

file = open('table_file_path')
json_dict = json.load(file)
query = dfquery.batch(json_dict)

tables = dfquery.tables()
table_1 = dfquery.table('table_1')
table_1.name('test_name').select('name').where({
    "key": "name",
    "operator": "=",
    "value": "dfquery"
})
tables.append(table_1)

table_2 = dfquery.table('table_2')
table_1.name('test_name').select('name').where({
    "key": "name",
    "operator": "!=",
    "value": "dfquery"
})

tables.append(table_2)

results = query.query(tables).build()

print(results)
```

### 테스트 코드

[tests](./tests)