from app.user import urls as user_urls
from app.post import urls as post_urls
from framework.fw.urls import Url, include


urlpatterns = [
    Url('user/', include=include(user_urls), namespace='user'),
    Url('posts/', include=include(post_urls), namespace='posts')
]