from dataclasses import dataclass
from typing import Type, List
from .view import View, Page404


@dataclass
class Url:
    url: str
    view: Type[View] | None = None
    include: list | None = None
    name: str | None = None
    namespace: str | None = None


def include(module) -> List[Url]:
    return module.urlpatterns


def get_view_from_urlpatterns(url_list: List[Url], url: str, view404: Type[View]) -> View:
    for path in url_list:
        if path.url in url:
            if path.view:
                return path.view(url.replace(path.url, ''))
            url = url.replace(path.url, '')
            print(url)
            return get_view_from_urlpatterns(path.include, url, view404)
    return view404()


start_urlpatterns = [
    Url('^/404', Page404, name='404'),
]
