from typing import Generator, Tuple
from .field import Expression

AND = ' AND '
OR = ' OR '
COMA = ', '


class Q:

    def __init__(self, exp: str = AND, **kwargs):
        self._exp = exp
        self._data = kwargs

    def __str__(self):
        kv_pair = [f'{k} = {v}' for k, v in self._data.items() if '__' not in k]
        for k, v in self._data.items():
            if v is not None:
                if '__' in k:
                    k = k.split('__')
                    if k[1] == 'btw':
                        kv_pair.append(
                            f'{k[0]} BETWEEN {v[0]} AND {v[-1]}\n\t')
                    if k[1] == 'in':
                        v = str(v)
                        if v[-2] == ',':
                            v = f'{v[:-2]})'
                        line = f'{k[0]} IN {v}\n\t'
                        kv_pair.append(line)
        return self._exp.join(kv_pair)

    def update_q(self) -> str:
        kv_pair = [f'{k} = "{v}"' for k, v in self._data.items()]
        return self._exp.join(kv_pair)

    def __bool__(self):
        return bool(self._data)


class BaseExp:
    name = None

    def add(self, *args) -> None:
        raise NotImplementedError

    def __bool__(self):
        raise NotImplementedError

    def _line(self) -> str:
        raise NotImplementedError

    def definition(self) -> str:
        return f'{self.name}\n\t{self._line()}\n'


class Select(BaseExp):
    name = 'SELECT'

    def __init__(self):
        self._data = []

    def add(self, *args) -> None:
        self._data.extend(args)

    def _line(self) -> str:
        return ', '.join(self._data)

    def __bool__(self):
        return bool(self._data)


class SelectD(BaseExp):
    name = 'SELECT DISTINCT'

    def __init__(self):
        self._data = []

    def add(self, *args) -> None:
        self._data.extend(args)

    def _line(self) -> str:
        return ', '.join(self._data)

    def __bool__(self):
        return bool(self._data)


class From(BaseExp):
    name = 'FROM'

    def __init__(self):
        self._data = []

    def add(self, *args) -> None:
        self._data.extend(args)

    def _line(self) -> str:
        return ', '.join(self._data)

    def __bool__(self):
        return bool(self._data)


class Update(BaseExp):
    name = 'UPDATE'

    def __init__(self):
        self._data = []

    def add(self, *args) -> None:
        self._data.extend(args)

    def _line(self) -> str:
        return ', '.join(self._data)

    def __bool__(self):
        return bool(self._data)


class Set(BaseExp):
    name = 'SET'

    def __init__(self, **kwargs):
        self._q = Q(COMA, **kwargs)

    def add(self, **kwargs) -> None:
        self._q = Q(COMA, **kwargs)

    def _line(self) -> str:
        return self._q.update_q()

    def __bool__(self):
        return bool(self._q)


class Where(BaseExp):
    name = 'WHERE'

    def __init__(self):
        self._q = None
        self.exp = None
        self.exp_list = []

    def add(self, exp: str = AND, expression: Expression = None, **kwargs) -> None:
        self.exp = exp
        if expression:
            self.exp_list.append(str(expression))
        if kwargs:
            self.exp_list.append(str(Q(exp, **kwargs)))


        # if expression is None:
        #     self._q = Q(exp, **kwargs)
        # else:
        #     self._q = str(expression)

    def _line(self) -> str:
        return self.exp.join(self.exp_list)

    def __bool__(self):
        return bool(self.exp_list)


class Insert(BaseExp):
    name = 'INSERT INTO'

    def __init__(self):
        self._data = []
        self._table = None

    def __call__(self, table) -> None:
        self._table = table

    def add(self, *args) -> None:
        self._data.extend(args)

    def __bool__(self):
        return bool(self._data)

    def definition(self) -> str:
        return f'{self.name} {self._table} ({self._line()})\n'

    def _line(self) -> str:
        return ', '.join(self._data)


class Values(BaseExp):
    name = 'VALUES'

    def __init__(self):
        self._data = []

    def add(self, *args) -> None:
        self._data.extend(args)

    def __bool__(self):
        return bool(self._data)

    def _line(self) -> str:
        return ', '.join(self._data)

    def definition(self) -> str:
        items = ','.join(['?'] * len(self._data))
        return f'{self.name} ({items})'


class Delete(BaseExp):
    name = 'DELETE FROM'

    def __init__(self):
        self._table = None

    def add(self, table: str) -> None:
        self._table = table

    def __bool__(self):
        return bool(self._table)

    def _line(self) -> str:
        return self._table


class Join(BaseExp):
    name = 'JOIN'
    'JOIN onetable ON onetable.id = twotable.one2'

    def __init__(self):
        self._data = []

    def add(self, table_name: str, related_tuple: Tuple[str, str]) -> None:
        self._data.append((table_name, related_tuple))

    def _line(self) -> str:
        for data in self._data:
            table_name, related_list = data
            field, foreign_table_field = related_list
            foreign_table, foreign_field = foreign_table_field
            yield f'{self.name}\n\t{foreign_table} ON {foreign_table}.{foreign_field} = {table_name}.{field}\n'

    def definition(self):
        return ''.join(self._line())

    def __bool__(self):
        return bool(self._data)


class Query:

    def __init__(self):
        self._data = {
            'select': Select(),
            'selectd': SelectD(),
            'from': From(),
            'update': Update(),
            'set': Set(),
            'delete': Delete(),
            'join': Join(),
            'where': Where(),
            'insert': Insert(),
            'values': Values()}

    def SELECT(self, *args):
        self._data['select'].add(*args)
        return self

    def SELECTD(self, *args):
        self._data['selectd'].add(*args)
        return self

    def FROM(self, *args):
        self._data['from'].add(*args)
        return self

    def WHERE(self, expression: Expression = None, **kwargs):
        self._data['where'].add(expression=expression, **kwargs)
        return self

    def INSERT(self, table, *args):
        self._data['insert'](table)
        self._data['insert'].add(*args)
        return self

    def UPDATE(self, *args):
        self._data['update'].add(*args)
        return self

    def SET(self, **kwargs):
        self._data['set'].add(**kwargs)
        return self

    def VALUES(self, *args):
        self._data['values'].add(*args)
        return self

    def DELETE(self, *args):
        self._data['delete'].add(*args)
        return self

    def JOIN(self, *args):
        self._data['join'].add(*args)
        return self

    def _lines(self) -> Generator:
        for k in self._data:
            if self._data[k]:
                yield self._data[k].definition()

    def __str__(self):
        return ''.join(self._lines())
