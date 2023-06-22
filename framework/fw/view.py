from typing import Type
from .exception import MethodError
from .request import Request
from .response import Response
from .template_engine import build_template
from ..orm.base_model import BaseModel
from ..orm.form import BaseForm


def redirect(request: Request, view: str) -> Response:
    from ..urls import urlpatterns
    host = request.environ.get('HOST')
    url = None
    for path in urlpatterns:
        print(view)
        print(path.name)
        if path.name == view:
            url = path.url[2:]
            break
    if not url:
        url = '404'
    return Response(status_code=303, headers={'Location': f'http://{host}/{url}'}, request=request)


class View:

    template_name: str | None = None
    extra_context: dict | None = None

    def __init__(self):
        self.context = self.get_context_data()
        self.request = None

    def get_context_data(self, **kwargs) -> dict:
        if self.extra_context:
            kwargs.update(self.extra_context)
        return kwargs

    def get(self, request: Request, *args, **kwargs) -> Response:
        self.request = request
        body = build_template(request, self.context, self.template_name)
        return Response(request=request, body=body)

    def post(self, request: Request, *args, **kwargs):
        pass

    def run(self, method, request):
        self.request = request
        if hasattr(self, method):
            return getattr(self, method)(request)
        raise MethodError


class ListView(View):

    model_class: Type[BaseModel]
    name_in_template: str = 'model'

    def get_context_data(self, **kwargs) -> dict:
        context = super(ListView, self).get_context_data(**kwargs)
        context[self.name_in_template] = self.model_class.objects.all()
        return context


class DetailView(View):

    model_class: Type[BaseModel]
    instance_id: int | None = None
    name_in_template: str = 'model'

    def get_context_data(self, **kwargs) -> dict:
        context = super(DetailView, self).get_context_data(**kwargs)
        context[self.name_in_template] = self.model_class.objects.get(self.model_class.id == self.instance_id)
        return context


class CreateView(View):
    form_class: Type[BaseModel]
    name_in_template: str = 'form'

    def get_context_data(self, **kwargs) -> dict:
        context = super(CreateView, self).get_context_data(**kwargs)
        context[self.name_in_template] = self.form_class()
        return context

    # def post(self, request: Request, *args, **kwargs):


class Page404(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(request, body='404')