import re
from typing import Any, Callable, List, Tuple
import settings
from framework.auth.security import get_password_hash
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
    check_type = None
    type = None
    html_type = None

    def __init__(
            self,
            foreign_key: None | str = None,
            nullable: bool = False,
            blank: bool = False,
            defaults: Any = None,
            unique: bool = False,
            verbose_name: str | None = None,
            placeholder: str | None = None,
            choices: List[Tuple[Any, str]] | None = None
    ):
        self._nullable = nullable
        self.blank = blank
        self._defaults = defaults
        self.foreign_key = str(foreign_key) if foreign_key is not None else None
        self.unique = unique
        self.placeholder = placeholder
        self.verbose_name = verbose_name
        self.choices = choices

    def __set_name__(self, owner, name):
        self.name = name
        self._owner = owner
        if not self.verbose_name:
            self.verbose_name = self.name

    def _create_expression(self, other, exp) -> Expression:
        if isinstance(other, str):
            other = f"'{other}'"
        elif other is None:
            other = 'Null'
            exp = 'IS'
        return Expression(f'{self._owner.model_name}.{self.name} {exp} {other}')

    def __eq__(self, other) -> Expression:
        return self._create_expression(other, '=')

    def __le__(self, other) -> Expression:
        return self._create_expression(other, '<=')

    def __lt__(self, other) -> Expression:
        return self._create_expression(other, '<')

    def __ge__(self, other) -> Expression:
        return self._create_expression(other, '>=')

    def __gt__(self, other) -> Expression:
        return self._create_expression(other, '>')


class Field(FieldBase):

    def get_line(self) -> str:
        if not self._nullable:
            self.type += ' NOT NULL'
        if self.unique:
            self.type += ' UNIQUE'
        return self.type

    def _type_check(self, obj, value) -> Any:
        if not isinstance(value, self.check_type) and not self.foreign_key:
            if not self._nullable:
                try:
                    value = self.check_type(value)
                except TypeError:
                    raise TypeError(
                        f'field {self.name} in {obj.model_name} have to be {self.check_type.__qualname__}'
                        f' but got {type(value)}')
        return value

    def __set__(self, obj, value) -> None:
        value = self._type_check(obj, value)
        obj.value_fields_dict[self.name] = value

    def __get__(self, obj, owner) -> Any:
        if obj is None:
            return self
        if not obj.value_fields_dict.get(self.name, False):
            if self._defaults is not None:
                if isinstance(self._defaults, Callable):
                    obj.value_fields_dict[self.name] = self._defaults()
                else:
                    obj.value_fields_dict[self.name] = self._defaults
            elif self._nullable:
                obj.value_fields_dict[self.name] = None
            else:
                raise ValueError(f'field {obj.__class__.__qualname__}.{self.name} cant be null')
        return obj.value_fields_dict[self.name]

    def __str__(self):
        return f'{self._owner.model_name}.{self.name}'

    def __neg__(self):
        return f'{self.__str__()} DESC'


class IdField(Field):
    type = 'INTEGER PRIMARY KEY AUTOINCREMENT'
    check_type = int | str
    html_type = 'number'


class IntField(Field):
    type = 'INTEGER'
    check_type = int
    html_type = 'number'


class TextField(Field):
    type = 'TEXT'
    check_type = str
    html_type = 'text'


class ImageField(TextField):
    html_type = 'file'

    def __get__(self, obj, owner):
        value = super(ImageField, self).__get__(obj, owner)
        if value:
            value = f'{settings.media_html}{obj.value_fields_dict[self.name]}'.replace('\\', '/')
            self.file_name = obj.value_fields_dict[self.name]
        return value

    def get_file_name_only(self):
        return self.file_name


class FloatField(Field):
    type = 'REAL'
    check_type = float
    html_type = 'number'


class PasswordField(Field):
    type = 'TEXT'
    check_type = str
    html_type = 'password'

    def __set__(self, obj, value) -> None:
        value = self._type_check(obj, value)
        if obj.new_instance:
            if len(value) < 6:
                raise ValueError('password is to short')
            obj.value_fields_dict[self.name] = get_password_hash(value)
        else:
            obj.value_fields_dict[self.name] = value


class EmailField(TextField):
    html_type = 'email'

    def __set__(self, obj, value) -> None:
        value = self._type_check(obj, value)
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        match = re.match(pattern, value)
        if match:
            obj.value_fields_dict[self.name] = value
        else:
            raise ValueError('not email format')


class DateField(Field):
    type = 'TEXT'
    html_type = 'date'

    def __set__(self, obj, value: datetime | str) -> None:
        if self._defaults is not None:
            if isinstance(value, datetime):
                obj.value_fields_dict[self.name] = str(value.isoformat())
            elif isinstance(value, str):
                try:
                    datetime.fromisoformat(value)
                except ValueError:
                    f'field {self.name} in {obj.model_name} have to be string in iso format'
                else:
                    obj.value_fields_dict[self.name] = value
            else:
                raise ValueError(
                    f'field {self.name} in {obj.model_name} have to be datetime or string'
                    f' but got {type(value)}')


class BoolField(IntField):
    html_type = 'checkbox'

    def __set__(self, obj, value: bool = False) -> None:
        if isinstance(value, bool):
            if value:
                obj.value_fields_dict[self.name] = 1
            else:
                obj.value_fields_dict[self.name] = 0
        elif value == '0' or value == '1':
            obj.value_fields_dict[self.name] = int(value)
        elif value == 0 or value == 1:
            obj.value_fields_dict[self.name] = value
        else:
            raise TypeError(f'boolean field should be bool but got {type(value)}')

    def __get__(self, obj, owner):
        if obj is None:
            return self
        if obj.value_fields_dict.get(self.name) is None:
            if self._defaults is not None:
                setattr(obj, self.name, self._defaults)
        if obj.value_fields_dict[self.name] == 1:
            return True
        return False
