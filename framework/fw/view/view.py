from typing import Type
from framework.fw.exception import MethodError
from framework.fw.request import Request
from framework.fw.response import Response
from framework.fw.template_engine.template_engine import build_template
from framework.fw.view.redirect import redirect
from framework.orm.base_model import BaseModel
from framework.orm.form import BaseForm


class View:
    template_name: str | None = None
    extra_context: dict | None = None
    success_redirect_url: str | None = None
    fail_redirect_url: str | None = None

    def __init__(self, arg: str | None = None):
        self.arg = arg
        self.context_from_context_manager = dict()
        self.request = None
        self.method = None

    def set_param(self, request, method):
        self.request = request
        self.method = method

    def get_context_data(self, **kwargs) -> dict:
        kwargs.update(self.context_from_context_manager)
        if self.extra_context:
            kwargs.update(self.extra_context)
        return kwargs

    def get(self, request: Request, *args, **kwargs) -> Response:
        context = self.get_context_data()
        body = build_template(request, context, self.template_name)
        return Response(request=request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        pass

    def dispatch(self):
        if hasattr(self, self.method):
            return getattr(self, self.method)(self.request)
        raise MethodError

    def run(self, method, request) -> Response:
        self.set_param(request, method)
        return self.dispatch()

    def render_to_response(self, context) -> Response:
        body = build_template(self.request, context, self.template_name)
        return Response(request=self.request, body=body)

    def success_redirect(self):
        return redirect(self.request, self.success_redirect_url)

    def fail_redirect(self):
        return redirect(self.request, self.fail_redirect_url)


class GenericView(View):
    model_class: Type[BaseModel]
    name_in_template: str = 'model'

    def get_queryset(self):
        queryset = self.model_class.objects
        return queryset


class ListView(GenericView):

    def get_context_data(self, **kwargs) -> dict:
        context = super(ListView, self).get_context_data(**kwargs)
        context[self.name_in_template] = self.get_queryset()
        return context


class DetailView(GenericView):

    def __init__(self, instance_id):
        self.id = instance_id
        super(DetailView, self).__init__()

    def get_object(self):
        return self.get_queryset().get(self.model_class.id == self.id)

    def get_context_data(self, **kwargs) -> dict:
        context = super(DetailView, self).get_context_data(**kwargs)
        context[self.name_in_template] = self.get_object()
        return context


class CreateView(GenericView):
    form_class: Type[BaseForm]
    name_in_template: str = 'form'

    def __init__(self, *args, **kwargs):
        super(CreateView, self).__init__(*args, **kwargs)

    def get_context_data(self, form: BaseForm | None = None, **kwargs) -> dict:
        context = super(CreateView, self).get_context_data(**kwargs)
        context[self.name_in_template] = form if form else self.get_form()
        return context

    @property
    def get_form(self):
        form = self.form_class(self.request)
        return form

    def post(self, request: Request, *args, **kwargs) -> Response:
        form = self.get_form(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form) -> Response:
        form.save()
        return redirect(self.request, self.success_redirect_url)

    def form_invalid(self, form: BaseForm) -> Response:
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


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
    def get_form(self) -> BaseForm:
        form = self.form_class(request=self.request, obj=self.get_object())
        return form

    def get_object(self) -> BaseModel:
        return self.get_queryset().get(self.model_class.id == self.id)

    def post(self, request: Request, *args, **kwargs) -> Response:
        form = self.get_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.request, self.success_redirect_url)
        return self.form_invalid(form)


class DeleteView(DetailView):
    model_class: Type[BaseModel]
    name_in_template: str = 'model'

    def get(self, request: Request, *args, **kwargs) -> Response:
        self.get_object().delete()
        return redirect(request, self.success_redirect_url)


class Page404(View):

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(request, body='404')
