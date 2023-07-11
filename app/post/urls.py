from app.post.view import PostCreate, PostList, PostDetail
from framework.fw.urls import Url

urlpatterns = [
    Url('new_post/', PostCreate, name='create_post'),
    Url('post/', PostList, name='posts_list'),
    Url('detail/', PostDetail, name='detail')
]