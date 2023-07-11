from app.urls import urlpatterns
from .fw.main import Framework
from settings import template_settings
from .fw.middleware import middlewares
from .fw.context_manager import context_managers

app = Framework(urls=urlpatterns, settings=template_settings,
                middlewares=middlewares, context_managers=context_managers)
