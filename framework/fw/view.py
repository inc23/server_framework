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
        if path.name == view:
            url = path.url[1:]
            break
    if not url:
        url = '404'
    return Response(status_code=303, headers={'Location': f'http://{host}/{url}'}, request=request)


class View:

    template_name: str | None = None
    extra_context: dict | None = None

    def __init__(self, *args, **kwargs):
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

    def __init__(self, instance_id):
        self.id = instance_id
        super(DetailView, self).__init__()

    model_class: Type[BaseModel]
    name_in_template: str = 'model'

    def get_context_data(self, **kwargs) -> dict:
        context = super(DetailView, self).get_context_data(**kwargs)
        context[self.name_in_template] = self.model_class.objects.get(self.model_class.id == self.id)
        return context


class CreateView(View):
    form_class: Type[BaseForm]
    name_in_template: str = 'form'
    redirect_page: str | None = None

    def get_context_data(self, **kwargs) -> dict:
        context = super(CreateView, self).get_context_data(**kwargs)
        context[self.name_in_template] = self.get_form()
        return context

    @property
    def get_form(self):
        form = self.form_class()
        return form

    def post(self, request: Request, *args, **kwargs) -> Response:
        form = self.get_form(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request, self.redirect_page)


class UpdateView(CreateView):

    def __init__(self, item_id):
        self.id = int(item_id)
        self.object = self.get_object()
        super(UpdateView, self).__init__()

    def get_context_data(self, **kwargs) -> dict:
        context = super(CreateView, self).get_context_data(**kwargs)
        context[self.name_in_template] = self.get_form()
        return context

    @property
    def get_form(self):
        form = self.form_class(obj=self.get_object())
        return form

    def get_object(self):
        class_object = self.form_class.model_class
        obj = class_object.objects.get(class_object.id == self.id)
        return obj

    def post(self, request: Request, *args, **kwargs) -> Response:
        form = self.get_form(request.POST)
        if form.is_valid():
            form.save()
        return redirect(self.request, self.redirect_page)


class Page404(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(request, body='404')