import re
from typing import Callable
from typing import List
from framework.fw.request import Request
from framework.fw.view import View, Page404
from .urls import Url, start_urlpatterns
from .exception import MethodError


class Framework:

    __slots__ = ('urls', 'settings')

    def __init__(self, urls: List[Url], settings: dict):
        self.urls = start_urlpatterns
        self.urls.extend(urls)
        self.settings = settings

    def __call__(self, environ: dict, start_response: Callable):
        view = self._get_view(environ)
        request = self._get_request(environ)
        response = self._get_response(environ, view, request)
        start_response(response.status_code, response.headers.items())
        return response.body

    @staticmethod
    def _prepare_url(url: str):
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, url: str):
        url = self._prepare_url(url)
        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view
        return Page404

    def _get_view(self, environ: dict):
        url = environ['PATH_INFO']
        view = self._find_view(url)
        return view()

    def _get_request(self, environ: dict):
        return Request(environ, self.settings)

    @staticmethod
    def _get_response(environ: dict, view: View, request: Request):
        method = environ['REQUEST_METHOD'].lower()
        if hasattr(view, method):
            return getattr(view, method)(request)
        raise MethodError

