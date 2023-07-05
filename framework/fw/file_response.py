import os

import settings
from framework.fw.request import Request
from framework.fw.response import Response


def file_response(request: Request, url: str) -> Response:
    url = url[1:]
    CHUNK_SIZE = 8192
    file_path = os.path.join(settings.BASE_DIR, url)
    if os.path.isfile(file_path):
        def file_generator():
            with open(file_path, 'rb') as file:
                while True:
                    chunk = file.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    yield chunk
        return Response(request=request, body=file_generator(), is_file=True)
    else:
        return Response(request=request, body=b'', is_file=True)
