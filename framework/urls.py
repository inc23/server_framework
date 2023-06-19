from .fw.urls import Url
from .view import Home, Hello, Get, Login


urlpatterns = [
    Url('^$', Home),
    Url('^/hello', Hello),
    Url('^/get', Get),
    Url('^/login', Login)
]