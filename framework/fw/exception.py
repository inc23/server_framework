class PageIsNotFound(Exception):
    code = 404
    text = 'page is not found'


class TemplateError(Exception):
    code = 404
    text = 'template is not found'


class MethodError(Exception):
    code = 404
    text = 'method not allowed'
