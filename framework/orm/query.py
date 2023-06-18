from typing import Generator

from framework.orm.field import Expression

AND = ' AND '
OR = ' OR '
COMA = ', '


class Q:

    def __init__(self, exp: str = AND, **kwargs):
        self.exp = exp
        self.data = kwargs

    def __str__(self):
        kv_pair = [f'{k} = {v}' for k, v in self.data.items() if '__' not in k]
        for k, v in self.data.items():
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
        return self.exp.join(kv_pair)

    def update_q(self) -> str:
        kv_pair = [f'{k} = "{v}"' for k, v in self.data.items()]
        return self.exp.join(kv_pair)

    def __bool__(self):
        return bool(self.data)


class BaseExp:
    name = None

    def add(self, *args):
        raise NotImplementedError

    def __bool__(self):
        raise NotImplementedError

    def line(self):
        raise NotImplementedError

    def definition(self):
        return f'{self.name}\n\t{self.line()}\n'


class Select(BaseExp):
    name = 'SELECT'

    def __init__(self):
        self.data = []

    def add(self, *args) -> None:
        self.data.extend(args)

    def line(self) -> str:
        return ','.join(self.data)

    def __bool__(self):
        return bool(self.data)


class SelectD(BaseExp):
    name = 'SELECT DISTINCT'

    def __init__(self):
        self.data = []

    def add(self, *args) -> None:
        self.data.extend(args)

    def line(self) -> str:
        return ','.join(self.data)

    def __bool__(self):
        return bool(self.data)


class From(BaseExp):
    name = 'FROM'

    def __init__(self):
        self.data = []

    def add(self, *args) -> None:
        self.data.extend(args)

    def line(self) -> str:
        return ','.join(self.data)

    def __bool__(self):
        return bool(self.data)


class Update(BaseExp):
    name = 'UPDATE'

    def __init__(self):
        self.data = []

    def add(self, *args) -> None:
        self.data.extend(args)

    def line(self) -> str:
        return ','.join(self.data)

    def __bool__(self):
        return bool(self.data)


class Set(BaseExp):
    name = 'SET'

    def __init__(self, **kwargs):
        self.q = Q(COMA, **kwargs)

    def add(self, **kwargs) -> None:
        self.q = Q(COMA, **kwargs)

    def line(self) -> str:
        return self.q.update_q()

    def __bool__(self):
        return bool(self.q)


class Where(BaseExp):
    name = 'WHERE'

    def __init__(self):
        self.q = None

    def add(self, exp: str = AND, expression: Expression = None, **kwargs) -> None:
        if expression is None:
            self.q = Q(exp, **kwargs)
        else:
            self.q = str(expression)[1:-1]

    def line(self) -> str:
        return str(self.q)

    def __bool__(self):
        return bool(self.q)


class Insert(BaseExp):
    name = 'INSERT INTO'

    def __init__(self):
        self.data = []
        self.table = None

    def __call__(self, table) -> None:
        self.table = table

    def add(self, *args) -> None:
        self.data.extend(args)

    def __bool__(self):
        return bool(self.data)

    def definition(self) -> str:
        return f'{self.name} {self.table} ({self.line()})\n'

    def line(self) -> str:
        return ', '.join(self.data)


class Values(BaseExp):
    name = 'VALUES'

    def __init__(self):
        self.data = []

    def add(self, *args) -> None:
        self.data.extend(args)

    def __bool__(self):
        return bool(self.data)

    def line(self) -> str:
        return ', '.join(self.data)

    def definition(self) -> str:
        items = ','.join(['?'] * len(self.data))
        return f'{self.name} ({items})'


class Delete(BaseExp):
    name = 'DELETE FROM'

    def __init__(self):
        self.table = None

    def add(self, table: str) -> None:
        self.table = table

    def __bool__(self):
        return bool(self.table)

    def line(self) -> str:
        return self.table


class Query:

    def __init__(self):
        self.data = {
            'select': Select(),
            'selectd': SelectD(),
            'from': From(),
            'update': Update(),
            'set': Set(),
            'delete': Delete(),
            'where': Where(),
            'insert': Insert(),
            'values': Values()}

    def SELECT(self, *args):
        self.data['select'].add(*args)
        return self

    def SELECTD(self, *args):
        self.data['selectd'].add(*args)
        return self

    def FROM(self, *args):
        self.data['from'].add(*args)
        return self

    def WHERE(self, expression: Expression = None, **kwargs):
        self.data['where'].add(expression=expression, **kwargs)
        return self

    def INSERT(self, table, *args):
        self.data['insert'](table)
        self.data['insert'].add(*args)
        return self

    def UPDATE(self, *args):
        self.data['update'].add(*args)
        return self

    def SET(self, **kwargs):
        self.data['set'].add(**kwargs)
        return self

    def VALUES(self, *args):
        self.data['values'].add(*args)
        return self

    def DELETE(self, *args):
        self.data['delete'].add(*args)
        return self

    def lines(self) -> Generator:
        for k in self.data:
            if self.data[k]:
                yield self.data[k].definition()

    def __str__(self) -> str:
        return ''.join(self.lines())
