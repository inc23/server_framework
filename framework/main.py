from .fw.main import Framework
from .urls import urlpatterns
from .settings import settings
from .fw.middleware import middlewares


app = Framework(urls=urlpatterns, settings=settings, middlewares=middlewares)