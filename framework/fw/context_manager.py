from framework.fw.request import Request
from settings import apps, app_name

context_managers = []


def add_context_manager(foo):
    context_managers.append(foo)
    return foo


@add_context_manager
def user_context_manager(context: dict, request: Request):
    context.update({'user': request.user})


for app in apps:
    try:
        __import__(f'{app_name}.{app}.context_manager')
    except ModuleNotFoundError:
        continue
