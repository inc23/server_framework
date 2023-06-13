from urllib.parse import parse_qs
from typing import AnyStr


class Request:

    def __init__(self, environ: dict, settings: dict):
        self.environ = environ
        self.settings = settings
        self._build_get_dict(environ['QUERY_STRING'])
        self._build_post_dict(environ['wsgi_input'])
        self.extra = dict()

    def __getattr__(self, item):
        return self.extra.get(item)

    def _build_get_dict(self, param: str):
        self.GET = parse_qs(param)

    def _build_post_dict(self, param: AnyStr):
        self.POST = parse_qs(param)