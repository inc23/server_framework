from app.post.model import Post
from framework.orm.form import BaseForm


class PostCreateForm(BaseForm):
    model_class = Post
    include_field = ('title', 'text', 'image', 'author', 'is_publish')

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['is_publish'].verbose_name = ' published '
