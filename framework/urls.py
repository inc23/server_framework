from .fw.urls import Url
from .view import Home, Hello, Get, Login, Test


urlpatterns = [
    Url('^$', Home),
    Url('^/hello', Hello),
    Url('^/get', Get),
    Url('^/login', Login),
    Url('^/test', Test)
]