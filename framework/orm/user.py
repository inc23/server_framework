from .field import FloatField, IntField, DateField, PasswordField, TextField, EmailField
from .base_model import BaseModel


class User(BaseModel):

    name = TextField()
    password = PasswordField()
    email = EmailField()
    created_at = DateField()