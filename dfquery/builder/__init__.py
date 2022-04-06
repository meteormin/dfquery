from dfquery.builder.builder import Builder
from dfquery.builder.build_parser import Parser
from pandas import DataFrame


def make(df: DataFrame = None) -> Builder:
    return Builder(Parser(df))
