from datetime import datetime
from framework.orm.base_model import BaseModel
from .orm.field import FloatField, IntField, DateField, TextField, PasswordField, EmailField, BoolField, ImageField


class User(BaseModel):
    name = TextField(nullable=True, verbose_name='name', placeholder='your name')
    last_name = TextField(nullable=False, verbose_name='last name', placeholder='your last name')
    password = PasswordField(placeholder='password')
    email = EmailField(nullable=False, unique=True, placeholder='your e-mail')
    created_at = DateField(defaults=datetime.utcnow)
    is_admin = BoolField(defaults=False)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Post(BaseModel):
    title = TextField(nullable=True, blank=True, verbose_name='title')
    text = TextField(nullable=False, verbose_name='text')
    image = ImageField(nullable=True, blank=True, verbose_name='image')
    author = IntField(nullable=False, foreign_key='user.id')
    created_at = DateField(defaults=datetime.utcnow)
    is_publish = BoolField(defaults=False)

    def __str__(self):
        return f'{self.title}'


class OneTable(BaseModel):
    one = FloatField(defaults=100000000000)
    two = IntField(nullable=True)
    date = DateField(defaults=datetime.utcnow)


class TwoTable(BaseModel):
    one2 = IntField(foreign_key='onetable.id')
    user = IntField(nullable=False, foreign_key='user.id')
