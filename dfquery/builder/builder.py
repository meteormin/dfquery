from pandas import DataFrame
from dfquery.builder.build_parser import Parser
from dfquery.abstracts import Attributes


class Builder:
    def __init__(self, parser: Parser):
        self._parser: Parser = parser

    @property
    def df(self):
        return self._parser.df

    @df.setter
    def df(self, df: DataFrame):
        self._parser.df = df

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, parser: Parser):
        self._parser = parser

    def build(self, attributes: Attributes) -> dict:
        result = {}

        for attr in attributes.all():
            result[attr.name] = {}
            select = attr.get_select()
            where = attr.get_where()
            for w in where:
                self._parser.where(w)
                selected = self._parser.select(select)
                result[attr.name].update(selected)

        return {
            attributes.table_name: result
        }
