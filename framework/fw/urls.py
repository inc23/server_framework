from dataclasses import dataclass
from typing import Type
from .view import View, Page404


@dataclass
class Url:
    url: str
    view: Type[View]
    name: str | None = None


start_urlpatterns = [
    Url('^/404', Page404, '404'),
]