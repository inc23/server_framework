from datetime import datetime
from app.user.model import User
from framework.orm.base_model import BaseModel
from framework.orm.field import TextField, ImageField, IntField, DateField, BoolField


class Post(BaseModel):
    title = TextField(nullable=True, blank=True, verbose_name='title')
    text = TextField(nullable=False, verbose_name='text')
    image = ImageField(nullable=True, blank=True, verbose_name='image')
    author = IntField(nullable=False, foreign_key=User.id)
    created_at = DateField(defaults=datetime.utcnow)
    is_publish = BoolField(defaults=False)

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def order_by(cls):
        return [-cls.id]
