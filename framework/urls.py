from .fw.urls import Url
from .view import Home, Hello, Get


urlpatterns = [
    Url('^$', Home),
    Url('^/hello', Hello),
    Url('^/get', Get)
]