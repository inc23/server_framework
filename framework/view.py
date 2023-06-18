from dataclasses import dataclass
from datetime import datetime
from .fw.view import View, Request
from .fw.response import Response
from .fw.template_engine import build_template

@dataclass
class Data:
    one: int | None
    two: int


data = []
for i in range(10):
    if i % 2:
        data.append(Data(i, i*10))
    else:
        data.append(Data(None, i))

data2 = []
for i in range(10):
    data2.append(Data(i*100, i*1000))


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

