from urllib.parse import parse_qs
from typing import AnyStr, Any


class Dict(dict):

    def __getitem__(self, item):
        try:
            result = super(Dict, self).__getitem__(item)
        except KeyError:
            return False
        return result[0]


class Request:

    def __init__(self, environ: dict, settings: dict):
        self.environ = environ
        self.settings = settings
        self._build_get_dict(environ['QUERY_STRING'])
        self._build_post_dict(environ['wsgi_input'])
        self.extra = dict()

    def __getattr__(self, item) -> Any:
        return self.extra.get(item)

    def _build_get_dict(self, param: str) -> None:
        self.GET = Dict(parse_qs(param))

    def _build_post_dict(self, param: AnyStr) -> None:
        self.POST = Dict(parse_qs(param))