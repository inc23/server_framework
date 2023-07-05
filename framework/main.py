from app.urls import urlpatterns
from .fw.main import Framework
from settings import template_settings
from .fw.middleware import middlewares

app = Framework(urls=urlpatterns, settings=template_settings, middlewares=middlewares)
