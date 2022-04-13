import pandas

from dfquery.abstracts import Core as AbsCore, DfQuery, Attributes as AbsAttributes, DictAble
from dfquery.attr import Attributes
from dfquery.builder import Builder
from dfquery.generator import Generator
from pandas import DataFrame
from typing import List, Dict, Union, Type
import copy


class Core(AbsCore):

    def __init__(self,
                 builder: Builder,
                 attributes: AbsAttributes
                 ):

        self._builder: Builder = builder
        self._table_name: str = ''
        self._df: DataFrame = pandas.DataFrame()
        self._attributes = attributes

    def from_dict(self, table_name: str, df_dict: dict, orient: str = None) -> 'Core':
        """
        make from dictionary
        :param table_name: 테이블이름
        :param df_dict: 생성할 Data
        :param orient: DataFrame 생성 시 요구되는 orient 파라미터와 동일
        :return: Core
        """
        self._table_name = table_name
        self._df = DataFrame.from_dict(df_dict, orient=orient)
        self._builder.df = self._df
        return self

    def from_records(self, table_name: str, data_list: List[dict]) -> 'Core':
        """
        make from records
        :param table_name: 테이블이름
        :param data_list: 생성할 Data
        :return: Core
        """
        self._table_name = table_name
        self._df = DataFrame.from_records(data_list)
        self._builder.df = self._df
        return self

    def from_df(self, table_name: str, df: DataFrame) -> 'Core':
        """
        make from DataFrame
        :param table_name:테이블이름
        :param df: 생성할 Data
        :return: Core
        """
        self._table_name = table_name
        self._df = df
        self._builder.df = self._df
        return self

    @property
    def df(self) -> DataFrame:
        return self._df

    @property
    def table_name(self) -> str:
        return self._table_name

    def get_query(self) -> Attributes:
        return self._attributes

    def query(self, query_dict: Union[dict, Generator]) -> 'Core':
        """
        parse query dictionary to dfquery.attr class
        :param query_dict: query로 사용될 딕셔너리
        :return: Core
        """
        attributes = []

        if isinstance(query_dict, Generator):
            query_dict = query_dict.to_dict()

        for name, value in query_dict.items():
            if isinstance(name, str) and isinstance(value, dict):
                self._attributes.append_child(len(attributes), name, value)
        return self

    def build(self):
        self._builder.df = self._df

        return self._builder.build(self._attributes)


class Collection(DfQuery):
    """
    다중 테이블 처리를 위한 컬렉션 클래스
    """

    def __init__(self,
                 builder: Builder,
                 attributes: Type[AbsAttributes],
                 ):
        self._builder: Builder = builder
        self._attributes: Type[AbsAttributes] = attributes
        self._children: List[Core] = []

    def make_children(self, data: Dict[str, Union[DataFrame, dict, List[dict]]], orient=None):
        self._children = []
        for name, v in data.items():
            child = self.make_child(name)
            if isinstance(v, DataFrame):
                child.from_df(name, v)
            elif isinstance(v, dict):
                child.from_dict(name, v, orient)
            elif isinstance(v, list):
                child.from_records(name, v)
            self._children.append(child)
        return self

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children: List[Core]):
        self._children = children

    def make_child(self, table_name: str) -> Core:
        return Core(copy.copy(self._builder), self._attributes(table_name))

    def get_by_table(self, table_name: str) -> Core:
        f = filter(lambda child: child.table_name == table_name, self._children)
        f_ls = list(f)
        return f_ls[0] if f_ls else None

    def query(self, query_dict: Union[Dict[str, dict], DictAble], table_name: str = None) -> Union['Collection', Core]:
        """

        :param query_dict: query dictionary
        :param table_name: 단일 테이블만 처리하고 싶을 경우 테이블 이름 지정
        :return: Collection
        """
        if isinstance(query_dict, DictAble):
            if isinstance(query_dict, Generator):
                query_dict = {query_dict.table: query_dict.to_dict()}
            else:
                query_dict = query_dict.to_dict()

        if table_name is not None:
            child = self.get_by_table(table_name)
            return child.query(query_dict[table_name])

        for table, query in query_dict.items():
            child = self.get_by_table(table)
            child.query(query)

        return self

    def build(self):
        result = {}
        for child in self._children:
            result.update(child.build())

        return result
