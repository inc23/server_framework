from framework.fw.urls import Url


urlpatterns = [
    Url('/login', Login, name='login'),
    Url('/users', Users, name='users'),
    Url('/user', UserItem, name='user'),
    Url('/new', UserCreate, name='create_user'),
]