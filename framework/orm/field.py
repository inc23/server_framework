from .security import get_password_hash
from datetime import datetime


class FieldBase:
    type = None


class Field(FieldBase):
    check_type = None

    def __init__(self, foreign_key: None | str = None):
        if foreign_key is not None:
            model, field = foreign_key.split('.')
            self.foreign_key = f'{model}({field})'
        else:
            self.foreign_key = None

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, obj, value) -> None:
        if isinstance(value, self.check_type):
            obj.new_model_instance_fields_dict[self.name] = value
        else:
            try:
                _value = self.check_type(value)
            except TypeError:
                raise ValueError(f'field {self.name} in {obj.model_name} have to be {self.check_type.__qualname__}'
                                 f' but got {type(value)}')
            else:
                obj.new_model_instance_fields_dict[self.name] = _value

    def __get__(self, obj, owner):
        return obj.new_model_instance_fields_dict[self.name]


class IdField(FieldBase):
    type = 'INTEGER PRIMARY KEY AUTOINCREMENT'


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
        if isinstance(value, str):
            obj.new_model_instance_fields_dict[self.name] = get_password_hash(value)
        else:
            try:
                _value = self.check_type(value)
            except TypeError:
                raise ValueError(f'field {self.name} in {obj.model_name} have to be str'
                                 f' but got {type(value)}')
            else:
                obj.new_model_instance_fields_dict[self.name] = get_password_hash(_value)


class DateField(Field):
    type = 'REAL'

    def __set__(self, obj, value: datetime) -> None:
        if isinstance(value, datetime):
            obj.new_model_instance_fields_dict[self.name] = value.timestamp()
        else:
            raise ValueError(f'field {self.name} in {obj.model_name} have to be datetime'
                             f' but got {type(value)}')

    def __get__(self, obj, owner):
        return datetime.fromtimestamp(obj.new_model_instance_fields_dict[self.name])