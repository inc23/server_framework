from app.user.form import UserCreateForm, UserUpdateForm
from app.user.model import User
from framework.auth.auth import authenticate, login
from framework.fw.request import Request
from framework.fw.view.message import message
from framework.fw.view.view import View, redirect, ListView, DetailView, CreateView, UpdateView


class Login(View):
    template_name = 'login.html'
    extra_context = {'a': 'aaaaaaa', 'b': None, "lst": [1, 2, None, None, None]}

    def post(self, request: Request, *args, **kwargs):
        email = request.POST.get('email')[0]
        password = request.POST.get('password')[0]
        user = authenticate(email, password)
        if user:
            login(request, user)
            message.success(request, 'login is success')
        else:
            message.warning(request, 'wrong login or password')
        return redirect(request, 'user:login')


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
    success_redirect_url = 'user:users'


class UserUpdate(UpdateView):
    form_class = UserUpdateForm
    extra_context = {'title': 'create user'}
    template_name = 'user_update.html'
    success_redirect_url = 'user:users'
