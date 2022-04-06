from dfquery.abstracts import Core as Abstract, DfQuery
from dfquery.abstracts import Attributes as AbsAttributes, AttrQuery as AbsAttrQuery
from dfquery.attr import Attributes
from dfquery.builder import Builder
from pandas import DataFrame
from typing import Type, List, Dict, Union
import copy


class Core(Abstract):
    _attributes_class: Type[AbsAttributes]
    _attr_class: Type[AbsAttrQuery]
    _builder: Builder
    _attributes: Attributes
    _table_name: str
    _df: DataFrame

    def __init__(self,
                 builder: Builder,
                 attributes: Type[AbsAttributes],
                 attr: Type[AbsAttrQuery]
                 ):
        self._builder = builder
        self._attributes_class = attributes
        self._attr_class = attr

    def from_dict(self, table_name: str, df_dict: dict, orient: str = None) -> 'Core':
        self._table_name = table_name
        self._df = DataFrame.from_dict(df_dict, orient=orient)
        self._builder.df = self._df
        return self

    def from_records(self, table_name: str, data_list: List[dict]):
        self._table_name = table_name
        self._df = DataFrame.from_records(data_list)
        self._builder.df = self._df
        return self

    def from_df(self, table_name: str, df: DataFrame) -> 'Core':
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

    def query(self, query_dict: dict) -> 'Core':
        attributes = []
        for name, value in query_dict.items():
            if isinstance(name, str) and isinstance(value, dict):
                attributes.append(self._attr_class(len(attributes), name, value))

        self._attributes = self._attributes_class(self._table_name, attributes)

        return self

    def build(self):
        self._builder.df = self._df

        return self._builder.build(self._attributes)


class Collection(DfQuery):
    _children: List[Core] = []
    _attributes_class: Type[AbsAttributes]
    _attr_class: Type[AbsAttrQuery]
    _builder: Builder

    def __init__(self,
                 builder: Builder,
                 attributes: Type[AbsAttributes],
                 attr: Type[AbsAttrQuery]
                 ):
        self._builder = builder
        self._attributes_class = attributes
        self._attr_class = attr

    def make_children(self, data: Dict[str, Union[DataFrame, dict, List[dict]]], orient=None):
        self._children = []
        for name, v in data.items():
            child = self.make_child()
            if isinstance(v, DataFrame):
                child.from_df(name, v)
            elif isinstance(v, dict):
                child.from_dict(name, v)
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

    def make_child(self):
        return Core(copy.copy(self._builder), self._attributes_class, self._attr_class)

    def get_by_table(self, table_name: str) -> Core:
        f = filter(lambda child: child.table_name == table_name, self._children)
        f_ls = list(f)
        return f_ls[0] if f_ls else None

    def query(self, query_dict: Dict[str, dict], table_name: str = None):
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
