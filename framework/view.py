from dataclasses import dataclass
from datetime import datetime
from .fw.view import View, Request
from .fw.response import Response
from .fw.template_engine import build_template
from .model import User
from .auth.security import verify_password


@dataclass
class Data:
    one: int | None
    two: int


data = []
for i in range(10):
    if i % 2:
        data.append(Data(i, i * 10))
    else:
        data.append(Data(None, i))

data2 = []
for i in range(10):
    data2.append(Data(i * 100, i * 1000))


class Home(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(
            request,
            {'time': str(datetime.utcnow()), 'lst': data, 'lst2': data2,
             'lst3': range(10), 'some_bool': True, 'session_id': request.session_id},
            'home.html'
        )
        return Response(request, body=body)


class Hello(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        body = build_template(
            request,
            {'name': 'incognito'},
            'hello.html'
        )
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        name = request.POST.get('name')
        if name:
            name = name[0]
        body = build_template(
            request,
            {'name': name},
            'hello.html'
        )
        return Response(request, body=body)


class Get(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        qs = str(request.GET.items())
        return Response(request, body=qs)


class Login(View):

    def get(self, request: Request, *args, **kwargs):
        body = build_template(
            request, {'text': 'login', 'unlogin': True}, 'login.html'
        )
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(User.email == email).all()
        if user:
            user = user[0]
            print(user.password)
            if verify_password(password, user.password):
                context = {'text': f'welcome {user.name}', 'unlogin': False}
            else:
                context = {'text': f'wrong', 'unlogin': True}
        else:
            context = {'text': f'wrong', 'unlogin': True}
        body = build_template(
            request, context, 'login.html'
        )
        return Response(request, body=body)
