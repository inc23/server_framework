from .fw.main import Framework
from .urls import urlpatterns
from .settings import template_settings
from .fw.middleware import middlewares

app = Framework(urls=urlpatterns, settings=template_settings, middlewares=middlewares)
