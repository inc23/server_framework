from .model import User
from .orm.form import BaseForm


class UserCreateForm(BaseForm):
    model_class = User
    include_field = ('name', 'last_name', 'password', 'email', 'is admin')


f = UserCreateForm()
