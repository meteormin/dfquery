from typing import List, Dict, Union, Type
from collections import UserList
from abstracts import DictAble


class Generator(DictAble):
    def __init__(self, table: str, name: str):
        self._table: str = table
        self._name: str = name
        self._select: List[str] = []
        self._where: List[Dict[str, Union[int, str, bool, float]]] = []

    @property
    def table(self):
        return self._table

    @property
    def name(self):
        return self._name

    def select(self, select: Union[List[str], str]) -> 'Generator':
        if isinstance(select, str):
            self._select.append(select)
        else:
            self._select = select
        return self

    def where(self,
              where: Union[List[Dict[str, Union[int, str, bool, float]]], Dict[
                  str, Union[int, str, bool, float]]]) -> 'Generator':
        if isinstance(where, dict):
            self._where.append(where)
        else:
            self._where = where
        return self

    def to_dict(self):
        return {
            self._name: {
                'select': self._select,
                'where': self._where
            }
        }


class Table(DictAble):
    _gen_class: Type[Generator] = Generator

    def __init__(self, table: str, gen_class: Type[Generator]):
        self._table: str = table
        self._gen: List[Generator] = []
        self._gen_class: Type[Generator] = gen_class

    @property
    def table(self):
        return self._table

    def name(self, name: str):
        self._gen.append(self._gen_class(self._table, name))
        gen = list(filter(lambda g: g.name == name, self._gen))

        return gen[0] if gen else None

    def names(self):
        return self._gen

    def to_dict(self):
        to_dict = {self._table: {}}
        for gen in self._gen:
            to_dict.get(self._table).update(gen.to_dict())

        return to_dict


class Tables(UserList, DictAble):
    def __init__(self, tables: List[Table] = None):
        super(Tables, self).__init__(tables)

    def __getitem__(self, i) -> Union[Table, Generator, 'Tables']:
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]

    def __setitem__(self, i, item: Union[Table, Generator]):
        self.data[i] = item

    def append(self, item: Union[Table, Generator]):
        self.data.append(item)

    def insert(self, i, item: Union[Table, Generator]):
        self.data.insert(i, item)

    def copy(self) -> 'Tables':
        return self.__class__(self.data)

    def extend(self, other: Union[List[Generator], List[Table]]):
        super(Tables, self).extend(other)

    def to_dict(self) -> dict:
        to_dict = {}
        for table in self.data:
            if isinstance(table, Table):
                to_dict.update(table.to_dict())

        return to_dict
