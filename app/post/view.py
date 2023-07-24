from app.mixin import UserCheckMixin, AuthorCheckMixin
from app.post.form import PostCreateForm, CommentCreateForm
from app.post.model import Post, Comment
from framework.fw.response import Response
from framework.fw.view.redirect import redirect
from framework.fw.view.view import CreateView, ListView, DetailView, DeleteView, UpdateView


class PostCreate(UserCheckMixin, CreateView):
    form_class = PostCreateForm
    extra_context = {'title': 'new post'}
    template_name = 'create_post.html'
    success_redirect_url = 'posts:posts_list'
    url_if_denied = 'posts:posts_list'


class PostList(ListView):
    model_class = Post
    template_name = 'posts.html'
    extra_context = {'title': 'posts list'}

    def get_queryset(self):
        queryset = Post.objects.select_related('author')
        return queryset


class PostDetail(CreateView):
    form_class = CommentCreateForm
    template_name = 'detail.html'
    extra_context = {'title': 'detail'}
    success_redirect_url = 'posts:detail'

    def get_context_data(self, **kwargs) -> dict:
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = Post.objects.select_related('author', 'comment', 'category').get(Post.id == self.arg)
        return context

    def form_valid(self, form) -> Response:
        form.post = Post.objects.get(Post.id == self.arg).id
        form.name = str(self.request.user)
        form.save()
        return redirect(self.request, self.success_redirect_url, arg=self.arg)


class MyPost(UserCheckMixin, ListView):
    model_class = Post
    extra_context = {'title': 'my post'}
    template_name = 'my_post_list.html'

    def get_queryset(self):
        return Post.objects.get(Post.id == self.request.user.id)


class MyPostDetail(AuthorCheckMixin, DetailView):
    model_class = Post
    template_name = 'detail.html'
    extra_context = {'title': 'detail'}
    url_if_denied = 'posts:posts_list'

    def get_context_data(self, **kwargs) -> dict:
        context = super(MyPostDetail, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(Post.id == self.arg)
        context['comments'] = Comment.objects.filter(Comment.post == context['post'].id)
        return context


class PostUpdate(AuthorCheckMixin, UpdateView):
    model_class = Post
    url_if_denied = 'posts:posts_list'
    extra_context = {'title': 'update'}


class DeletePost(AuthorCheckMixin, DeleteView):
    model_class = Post
    url_if_denied = 'posts:posts_list'
