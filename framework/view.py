from .form import UserCreateForm, UserUpdateForm, PostCreateForm
from .fw.view import View, Request, ListView, DetailView, redirect, CreateView, UpdateView
from .auth.auth import authenticate, login
from .model import User, Post


class Login(View):
    template_name = 'login.html'
    extra_context = {'a': 'aaaaaaa', 'b': None, "lst": [1, 2, None, None, None]}

    def post(self, request: Request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email, password)
        if user:
            login(request, user)
        return redirect(request, 'login')


class Users(ListView):
    model_class = User
    extra_context = {'title': 'users'}
    template_name = 'users.html'


class UserItem(DetailView):
    model_class = User
    extra_context = {'title': 'user'}
    template_name = 'user.html'


class UserCreate(CreateView):
    form_class = UserCreateForm
    extra_context = {'title': 'create user'}
    template_name = 'create_user.html'
    redirect_page = 'users'


class UserUpdate(UpdateView):
    form_class = UserUpdateForm
    extra_context = {'title': 'create user'}
    template_name = 'user_update.html'
    redirect_page = 'users'


class PostCreate(CreateView):
    form_class = PostCreateForm
    extra_context = {'title': 'new post'}
    template_name = 'create_post.html'
    redirect_page = 'users'


class PostList(ListView):
    model_class = Post
    template_name = 'posts.html'
    extra_context = {'title': 'posts'}

    def get_queryset(self):
        queryset = Post.objects.select_related('author')
        return queryset