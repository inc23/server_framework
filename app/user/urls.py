from app.user.view import Login, Users, UserDetail, UserCreate
from framework.fw.urls import Url


urlpatterns = [
    Url('login/', Login, name='login'),
    Url('users/', Users, name='users'),
    Url('user/', UserDetail, name='user'),
    Url('new/', UserCreate, name='create_user'),
]