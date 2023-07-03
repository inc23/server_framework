from app.post.form import PostCreateForm
from app.post.model import Post
from framework.fw.view import CreateView, ListView


class PostCreate(CreateView):
    form_class = PostCreateForm
    extra_context = {'title': 'new post'}
    template_name = 'create_post.html'
    redirect_page = 'users'


class PostList(ListView):
    model_class = Post
    template_name = 'posts.html'
    extra_context = {'title': 'posts list'}

    def get_queryset(self):
        queryset = Post.objects.select_related('author')
        return queryset
