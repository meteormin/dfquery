from dfquery.abstracts import Attributes as AbsAttributes, AttrQuery as AbsAttrQuery
from typing import List


class Attributes(AbsAttributes):
    def __init__(self, table_name: str, attributes: List[AbsAttrQuery]):
        super(Attributes, self).__init__(table_name, attributes)

    @property
    def table_name(self) -> str:
        return self._table_name

    def get_by_index(self, idx: int):
        return self._attributes[idx]

    def get_by_select(self, select: str):
        f = filter(lambda x: select in x.get_select(), self._attributes)
        f_ls = list(f)
        return f_ls[0] if f_ls else None

    def get_by_name(self, name: str):
        f = filter(lambda x: name == x.get_name(), self._attributes)
        f_ls = list(f)
        return f_ls[0] if f_ls else None


class AttrQuery(AbsAttrQuery):
    def __init__(self, index: int, name: str, attr_dict: dict = None):
        super(AttrQuery, self).__init__(index, name, attr_dict)

    @property
    def name(self):
        return self._name

    def select(self, select: List[str]) -> 'AttrQuery':
        self._select.extend(select)
        return self

    def where(self, where: List[dict]) -> 'AttrQuery':
        self._where.extend(where)
        return self

    def get_where(self):
        return self._where

    def get_select(self):
        return self._select
