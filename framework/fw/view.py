from .request import Request
from .response import Response


class View:

    def get(self, request: Request, *args, **kwargs):
        pass

    def post(self, request: Request, *args, **kwargs):
        pass


class Page404(View):

    def get(self, request: Request, *args, **kwargs):
        return Response(request, body='404')