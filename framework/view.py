from .fw.view import View, Request
from .fw.response import Response


class Home(View):

    def get(self, request: Request, *args, **kwargs):
        return Response(request, body='hello')


class Hello(View):

    def get(self, request: Request, *args, **kwargs):
        pass


class Get(View):

    def get(self, request: Request, *args, **kwargs):
        qs = str(request.GET.items())
        return Response(request, body=qs)

