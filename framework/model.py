from datetime import datetime
from framework.orm.base_model import BaseModel, MetaModel
from framework.orm.field import FloatField, IntField, DateField, TextField, PasswordField, EmailField, BoolField


class User(BaseModel):
    name = TextField(nullable=False, verbose_name='name')
    last_name = TextField(nullable=False, verbose_name='last name')
    password = PasswordField()
    email = EmailField(nullable=False, unique=True)
    created_at = DateField(defaults=datetime.utcnow)
    is_admin = BoolField(defaults=False)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class OneTable(BaseModel):
    one = FloatField(defaults=100000000000)
    two = IntField(nullable=True)
    date = DateField(defaults=datetime.utcnow)


class TwoTable(BaseModel):
    one = IntField(foreign_key='onetable.id')


