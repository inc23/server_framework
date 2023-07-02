import os

from framework import settings
from framework.fw.request import Request
from framework.fw.response import Response


def file_response(request: Request, url: str) -> Response:
    url = url[1:]
    file_path = os.path.join(settings.main_path, url)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            file_content = file.read()
    else:
        file_content = b''
    return Response(request=request, body=file_content, is_file=True)
