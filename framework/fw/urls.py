from dataclasses import dataclass
from typing import Type
from .view import View, Page404


def include(module):
    return module.urlpatterns


@dataclass
class Url:
    url: str
    view: Type[View] | None = None
    urlpatterns: list | None = None
    name: str | None = None
    namespace: str | None = None



start_urlpatterns = [
    Url('^/404', Page404, name='404'),
]