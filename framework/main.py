from .fw.main import Framework
from .urls import urlpatterns
from .settings import settings


app = Framework(urls=urlpatterns, settings=settings)