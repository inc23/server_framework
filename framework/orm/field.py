class Field:
    type = None

    def __init__(self, foreign_key: None | str = None):
        if foreign_key is not None:
            model, field = foreign_key.split('.')
            self.foreign_key = f'{model}({field})'
        else:
            self.foreign_key = None


class IdField(Field):
    type = 'INTEGER PRIMARY KEY AUTOINCREMENT'


class IntField(Field):
    type = 'INTEGER'


class TextField(Field):
    type = 'TEXT'


class ImageField(Field):
    type = 'TEXT'


class FloatField(Field):
    type = 'REAL'


class PasswordField(Field):
    type = 'TEXT'


class DateField(Field):
    type = 'REAL'

