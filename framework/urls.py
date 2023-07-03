from app.post.view import PostCreate, PostList
from app.user.view import Login, Users, UserItem, UserCreate, UserUpdate
from .fw.urls import Url


urlpatterns = [
    Url('/login', Login, 'login'),
    Url('/users', Users, 'users'),
    Url('/user', UserItem, 'user'),
    Url('/new', UserCreate, 'create_user'),
    Url('/update', UserUpdate, 'create_user'),
    Url('/new_post', PostCreate, 'create_post'),
    Url('/posts', PostList, 'posts_list')
]

