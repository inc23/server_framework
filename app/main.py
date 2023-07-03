from framework.fw.main import Framework
from .urls import urlpatterns
from framework.settings import template_settings
from framework.fw.middleware import middlewares

app = Framework(urls=urlpatterns, settings=template_settings, middlewares=middlewares)
