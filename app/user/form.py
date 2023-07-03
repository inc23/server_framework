from app.user.model import User
from framework.orm.form import BaseForm


class UserCreateForm(BaseForm):
    model_class = User
    include_field = ('name', 'last_name', 'password', 'email', 'is_admin')


class UserUpdateForm(BaseForm):
    model_class = User
    include_field = ('name', 'last_name', 'email', 'is_admin')
