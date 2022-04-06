from pandas import DataFrame
from typing import Union, List, Dict
from dfquery.attr import Attributes, AttrQuery
from dfquery.core import Core, Collection
import dfquery.builder


def make(table_name: str, data: Union[DataFrame, dict, list] = None, orient: str = None) -> Core:
    core_obj = Core(builder.make(), Attributes, AttrQuery)
    if isinstance(data, DataFrame):
        core_obj.from_df(table_name, data)
    elif isinstance(data, dict):
        core_obj.from_dict(table_name, data, orient)
    elif isinstance(data, list):
        core_obj.from_records(table_name, data)

    return core_obj


def batch(data: Dict[str, Union[DataFrame, dict, List[dict]]], orient=None) -> Collection:
    collection = Collection(builder=builder.make(), attributes=Attributes, attr=AttrQuery)
    return collection.make_children(data, orient)
