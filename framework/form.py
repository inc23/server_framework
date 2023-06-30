from .model import User, Post
from .orm.form import BaseForm


class UserCreateForm(BaseForm):
    model_class = User
    include_field = ('name', 'last_name', 'password', 'email', 'is_admin')


class UserUpdateForm(BaseForm):
    model_class = User
    include_field = ('name', 'last_name', 'email', 'is_admin')


class PostCreateForm(BaseForm):
    model_class = Post
    include_field = ('title', 'text', 'image', 'author', 'is_publish')

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['is_publish'].verbose_name = ' published '
