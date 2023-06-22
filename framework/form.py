from .model import User
from .orm.form import BaseForm


class UserCreateForm(BaseForm):
    model_class = User
    include_field = 'all'


f = UserCreateForm()

print(f.id)