from pandas import DataFrame


class Parser:
    _df: DataFrame

    def __init__(self, df: DataFrame = None):
        self._df = df

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, df: DataFrame):
        self._df = df

    def select(self, select: list) -> list:
        selected = []
        for df_idx, row in self._df.iterrows():
            selected_row = {}
            if '*' in select:
                selected_row.update(row.to_dict())
            else:
                for s in select:
                    selected_row.update({s: row[s]})
            selected.append(selected_row)
        return selected

    def where(self, where: dict) -> DataFrame:
        str_query = ''
        column = None
        operator = None
        value = None

        for k, v in where.items():
            if k == 'key':
                column = f"`{v}`"
            elif k == 'operator':
                if v == 'like':
                    operator = 'str'
                else:
                    operator = f"{v}"
            elif k == 'value':
                value = str(v)
                if not value.isnumeric():
                    value = f"'{str(v)}'"

        if column is None or operator is None or value is None:
            return self._df

        if operator == 'str':
            operator = self.parse_wild_card(value)

            str_query += column + operator
        else:
            str_query += f"{column} {operator} {value}"

        self._df = self._df.query(str_query)
        return self._df

    @staticmethod
    def parse_wild_card(value: str):
        if '*' not in value:
            return

        value = value.replace("'", '')
        index = value.find('*')

        if index == -1:
            return

        if index == 0 and value[len(value) - 1] != '*':
            func = 'str.endswith'
        elif index == 0 and index == len(value) - 1:
            func = 'str.startswith'
        else:
            func = 'str.contains'

        value = value.replace('*', '')

        return f".{func}('{value}', na=False)"
