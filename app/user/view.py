from app.user.form import UserCreateForm, UserUpdateForm
from app.user.model import User
from framework.auth.auth import authenticate, login
from framework.fw.request import Request
from framework.fw.view.view import View, redirect, ListView, DetailView, CreateView, UpdateView
from app.mixin import AdminCheckMixin


class Login(View):
    template_name = 'login.html'
    extra_context = {'title': 'login'}

    def post(self, request: Request, *args, **kwargs):
        email = request.POST.get('email')[0]
        password = request.POST.get('password')[0]
        user = authenticate(email, password)
        if user:
            login(request, user)
        return redirect(request, 'user:login')


class Users(AdminCheckMixin, ListView):
    model_class = User
    extra_context = {'title': 'users'}
    template_name = 'users.html'


class UserDetail(DetailView):
    model_class = User
    extra_context = {'title': 'user'}
    template_name = 'user.html'


class UserCreate(CreateView):
    form_class = UserCreateForm
    extra_context = {'title': 'create user'}
    template_name = 'create_user.html'
    success_redirect_url = 'user:users'


class AdminUserUpdate(AdminCheckMixin, UpdateView):
    form_class = UserUpdateForm
    extra_context = {'title': 'update user'}
    template_name = 'user_update.html'
    success_redirect_url = 'user:users'


class UserUpdate(UpdateView):
    form_class = UserUpdateForm
    extra_context = {'title': 'update my profile'}
    template_name = 'user_update.html'
    success_redirect_url = 'user:users'

    def get_object(self):
        self.id = self.request.user.id
        return super(UserUpdate, self).get_object()
