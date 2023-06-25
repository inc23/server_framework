from .fw.urls import Url
from .view import Login, Users, UserItem, UserCreate, UserUpdate


urlpatterns = [
    Url('/login', Login, 'login'),
    Url('/users', Users, 'users'),
    Url('/user', UserItem, 'user'),
    Url('/new', UserCreate, 'create_user'),
    Url('/update', UserUpdate, 'create_user')
]

