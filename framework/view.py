from datetime import datetime
from .fw.view import View, Request
from .fw.response import Response
from .fw.template_engine import build_template


class Home(View):

    def get(self, request: Request, *args, **kwargs):
        body = build_template(
            request,
            {'time': str(datetime.utcnow()), 'lst': range(10), 'session_id': request.session_id},
            'home.html'
        )
        return Response(request, body=body)


class Hello(View):

    def get(self, request: Request, *args, **kwargs):
        body = build_template(
            request,
            {'name': 'incognito'},
            'hello.html'
        )
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs):
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

    def get(self, request: Request, *args, **kwargs):
        qs = str(request.GET.items())
        return Response(request, body=qs)

