import re
from typing import Callable, List, Type
from framework.fw.request import Request
from framework.fw.view import View, Page404
from .response import Response
from .urls import Url, start_urlpatterns
from .exception import MethodError
from .middleware import Middleware
from ..orm.base_model import MetaModel


class Framework:

    __slots__ = ('urls', 'settings', 'middlewares')

    def __init__(self, urls: List[Url], settings: dict, middlewares: List[Type[Middleware]]):
        self.urls = start_urlpatterns
        self.urls.extend(urls)
        self.settings = settings
        self.middlewares = middlewares
        MetaModel.create_tables()

    def __call__(self, environ: dict, start_response: Callable) -> bytes:
        view = self._get_view(environ)
        request = self._get_request(environ)
        self._to_request(request)
        response = self._get_response(environ, view, request)
        self._to_response(response)
        start_response(response.status_code, response.headers.items())
        return response.body

    @staticmethod
    def _prepare_url(url: str) -> str:
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, url: str) -> Type[View]:
        url = self._prepare_url(url)
        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view
        return Page404

    def _get_view(self, environ: dict) -> View:
        url = environ['PATH_INFO']
        view = self._find_view(url)
        return view()

    def _get_request(self, environ: dict) -> Request:
        return Request(environ, self.settings)

    @staticmethod
    def _get_response(environ: dict, view: View, request: Request) -> Response:
        method = environ['REQUEST_METHOD'].lower()
        if hasattr(view, method):
            return getattr(view, method)(request)
        raise MethodError

    def _to_response(self, response: Response) -> None:
        for middleware in self.middlewares:
            middleware().to_response(response)

    def _to_request(self, request: Request) -> None:
        for middleware in self.middlewares:
            middleware().to_request(request)


