from app.post.view import PostCreate, PostList
from app.user.view import Login, Users, UserItem, UserCreate, UserUpdate
from framework.fw.urls import Url, include


urlpatterns = [
    Url('/login', Login, name='login'),
    Url('/users', Users, name='users'),
    Url('/user', UserItem, name='user'),
    Url('/new', UserCreate, name='create_user'),
    Url('/update', UserUpdate, name='create_user'),
    Url('/new_post', PostCreate, name='create_post'),
    Url('/posts', PostList, name='posts_list')
]

