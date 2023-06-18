import re
from typing import Any, Callable
from .security import get_password_hash
from datetime import datetime


class Expression:
    def __init__(self, expression):
        self.expression = expression

    def __and__(self, other):
        return Expression(f'({self.expression} AND {other.expression})')

    def __or__(self, other):
        return Expression(f'({self.expression} OR {other.expression})')

    def __str__(self):
        return self.expression


class FieldBase:
    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner

    def __eq__(self, other) -> Expression:
        return Expression(f'{self.name} = {other}')

    def __le__(self, other) -> Expression:
        return Expression(f'{self.name} <= {other}')

    def __lt__(self, other) -> Expression:
        return Expression(f'{self.name} < {other}')

    def __ge__(self, other) -> Expression:
        return Expression(f'{self.name} >= {other}')

    def __gt__(self, other) -> Expression:
        return Expression(f'{self.name} > {other}')


class Field(FieldBase):
    check_type = None
    type = None

    def __init__(
            self,
            foreign_key: None | str = None,
            nullable: bool = True,
            defaults: Any = None
    ):
        self.nullable = nullable
        self.defaults = defaults
        if foreign_key is not None:
            model, field = foreign_key.split('.')
            self.foreign_key = f'{model}({field})'
        else:
            self.foreign_key = None

    def __set__(self, obj, value) -> None:
        if value is not None:
            if not isinstance(value, self.check_type):
                try:
                    value = self.check_type(value)
                except TypeError:
                    raise ValueError(
                        f'field {self.name} in {obj.model_name} have to be {self.check_type.__qualname__}'
                        f' but got {type(value)}')
        else:
            if not self.nullable:
                raise ValueError('this field cant bu null')
        obj.value_fields_dict[self.name] = value

    def __get__(self, obj, owner):
        if obj is not None:
            if not obj.value_fields_dict.get(self.name, False):
                if self.defaults is not None:
                    if isinstance(self.defaults, Callable):
                        obj.value_fields_dict[self.name] = self.defaults()
                    else:
                        obj.value_fields_dict[self.name] = self.defaults
                elif self.nullable:
                    obj.value_fields_dict[self.name] = None
            return obj.value_fields_dict[self.name]
        return self


class IdField(Field):
    type = 'INTEGER PRIMARY KEY AUTOINCREMENT'
    check_type = int | str


class IntField(Field):
    type = 'INTEGER'
    check_type = int


class TextField(Field):
    type = 'TEXT'
    check_type = str


class ImageField(TextField):
    pass


class FloatField(Field):
    type = 'REAL'
    check_type = float


class PasswordField(Field):
    type = 'TEXT'

    def __set__(self, obj, value) -> None:
        if not isinstance(value, str):
            try:
                value = self.check_type(value)
            except TypeError:
                raise ValueError(
                    f'field {self.name} in {obj.model_name} have to be str'
                    f' but got {type(value)}')
        if len(value) < 6:
            raise Exception('password is to short')
        obj.value_fields_dict[self.name] = get_password_hash(value)


class EmailField(TextField):

    def __set__(self, obj, value):
        if not isinstance(value, str) and not self.nullable:
            try:
                value = self.check_type(value)
            except TypeError:
                raise ValueError(
                    f'field {self.name} in {obj.model_name} have to be str'
                    f' but got {type(value)}')
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        match = re.match(pattern, value)
        if match:
            obj.value_fields_dict[self.name] = value
        else:
            raise Exception('not email format')


class DateField(Field):
    type = 'REAL'

    def __set__(self, obj, value: datetime) -> None:
        if self.defaults is not None:
            if isinstance(value, datetime):
                obj.value_fields_dict[self.name] = value.timestamp()
            elif isinstance(value, float):
                obj.value_fields_dict[self.name] = datetime.fromtimestamp(
                    value)
            else:
                raise ValueError(
                    f'field {self.name} in {obj.model_name} have to be datetime'
                    f' but got {type(value)}')

    def __get__(self, obj, owner):
        time = super(DateField, self).__get__(obj, owner)
        if isinstance(time, datetime):
            obj.value_fields_dict[self.name] = datetime.timestamp(time)
        return time
