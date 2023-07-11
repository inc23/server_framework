from framework.fw.request import Request


def user_context_manager(context: dict, request: Request):
    context.update({'user': request.user})


context_managers = [user_context_manager]