from framework.fw.request import Request
from framework.fw.response import Response


def redirect(request: Request, spacename_name: str, arg=None) -> Response:
    from app.urls import urlpatterns
    host = request.environ.get('HOST')
    url = None
    if ':' in spacename_name:
        spacename, name = spacename_name.split(':')
        for path in urlpatterns:
            if path.namespace == spacename:
                _url = path.url
                for pth in path.include:
                    if pth.name == name:
                        _url += pth.url
                        url = _url
                        break
    else:
        for path in urlpatterns:
            if path.name == spacename_name:
                url = path.url
    if not url:
        url = '404'
    redirect_url = f'http://{host}/{url}{arg}' if arg else f'http://{host}/{url}'
    return Response(status_code=303, headers={'Location': redirect_url}, request=request)
