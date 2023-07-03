from datetime import datetime
from framework.orm.field import DateField, PasswordField, TextField, EmailField, BoolField
from framework.orm.base_model import BaseModel


class BaseUser(BaseModel):

    name = TextField(nullable=False)
    last_name = TextField(nullable=False)
    password = PasswordField(nullable=False)
    email = EmailField(nullable=False)
    created_at = DateField(defaults=datetime.utcnow)
    is_admin = BoolField()
