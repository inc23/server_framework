from .fw.urls import Url
from .view import Login, Users, UserItem, UserCreate, UserUpdate, PostCreate


urlpatterns = [
    Url('/login', Login, 'login'),
    Url('/users', Users, 'users'),
    Url('/user', UserItem, 'user'),
    Url('/new', UserCreate, 'create_user'),
    Url('/update', UserUpdate, 'create_user'),
    Url('/new_post', PostCreate, 'create_post')
]

