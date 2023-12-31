import datetime
from framework.orm.field import DateField, PasswordField, TextField, EmailField, BoolField
from framework.orm.base_model import BaseModel


class User(BaseModel):

    name = TextField(nullable=False)
    last_name = TextField(nullable=False)
    password = PasswordField(nullable=False)
    email = EmailField(nullable=False)
    created_at = DateField(defaults=datetime.datetime)
    is_admin = BoolField()
