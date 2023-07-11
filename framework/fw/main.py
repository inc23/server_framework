from typing import Callable, List, Type
from .request import Request
from framework.fw.view.view import View, Page404
from .response import Response
from .urls import Url, start_urlpatterns, get_view_from_urlpatterns
from .middleware import Middleware
from ..orm.base_model import MetaModel
from .file_response import file_response


class Framework:

    __slots__ = ('_urls', '_settings', '_middlewares', 'context_managers')

    def __init__(self, urls: List[Url], settings: dict, middlewares: List[Type[Middleware]], context_managers: list):
        self._urls = start_urlpatterns
        self._urls.extend(urls)
        self._settings = settings
        self._middlewares = middlewares
        self.context_managers = context_managers
        MetaModel.create_tables()

    def __call__(self, environ: dict, start_response: Callable) -> bytes:
        request = self._get_request(environ)
        if environ['SEC_FETCH_DEST'] != 'document':
            response = self._get_file_response(environ, request)
        else:
            view = self._get_view(environ)
            self._to_request(request)
            self._apply_context_manager(view, request)
            response = self._get_response(environ, view, request)
            self._to_response(response)
        start_response(response.status_code, response.headers.items())
        return response.body

    @staticmethod
    def _prepare_url(url: str) -> str:
        if url[-1] != '/':
            url = f'{url}/'
        return url[1:]

    def _find_view(self, url: str) -> View:
        url = self._prepare_url(url)
        return get_view_from_urlpatterns(self._urls, url, Page404)

    def _get_view(self, environ: dict) -> View:
        url = environ['PATH_INFO']
        view = self._find_view(url)
        return view

    def _get_request(self, environ: dict) -> Request:
        return Request(environ, self._settings, self._urls)

    @staticmethod
    def _get_response(environ: dict, view: View, request: Request) -> Response:
        method = environ['REQUEST_METHOD'].lower()
        return view.run(method, request)

    @staticmethod
    def _get_file_response(environ, request):
        url = environ['PATH_INFO']
        return file_response(request, url)

    def _apply_context_manager(self, view: View, request: Request):
        for context_manager in self.context_managers:
            context_manager(view.context_from_context_manager, request)

    def _to_response(self, response: Response) -> None:
        for middleware in self._middlewares:
            middleware().to_response(response)

    def _to_request(self, request: Request) -> None:
        for middleware in self._middlewares:
            middleware().to_request(request)
