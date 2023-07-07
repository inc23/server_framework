from typing import Any, Tuple, Generator
from .request import Request


class Headers:

    def __init__(self):
        self._data_dict = dict()
        self._key = 0

    def update(self, data: dict) -> None:
        for k, v in data.items():
            if k == 'Set-Cookie':
                self._data_dict.update({self._key: {k: v}})
                self._key += 1
            else:
                self._data_dict.update({k: v})

    def _get_headers(self) -> Tuple[str, str]:
        for k, v in self._data_dict.items():
            if isinstance(k, int):
                for key, val in v.items():
                    k, v = key, val
            yield k, v

    def items(self):
        return [(k, v) for k, v in self._get_headers()]


class Response:

    def __init__(self, request: Request, status_code: int = 200, headers=None, body: str | bytes | Generator = '',
                 is_file: bool = False):
        self.is_file = is_file
        self.request = request
        self.status_code = status_code
        self.headers = Headers()
        self.body = b''
        self._set_headers()
        if headers is not None:
            self.headers.update(headers)
        if body:
            self._set_body(body)
        self.extra = dict()

    def __getattr__(self, item) -> Any:
        return self.extra.get(item)

    def _set_headers(self) -> None:
        if self.is_file:
            if self.request.environ['SEC_FETCH_DEST'] == 'style':
                self.headers.update({
                    'Cache-Control': 'max-age=8380800',
                    'Content-Type': 'text/css'
                })
            elif self.request.environ['SEC_FETCH_DEST'] == 'script':
                self.headers.update({
                    'Cache-Control': 'max-age=8380800',
                    'Content-Type': 'application/javascript'
                })
            else:
                file_name = self.request.environ['PATH_INFO'].rsplit('/', maxsplit=1)[-1]
                self.headers.update({
                    'Content-Type': 'application/octet-stream',
                    'Content-Disposition': f'attachment; filename="{file_name}"',
                })

        else:
            self.headers.update({
                'Content-Type': 'text/html; charset=utf-8',
                "Content-Length": '0'
            })

    def _set_body(self, body) -> None:
        if isinstance(body, str):
            self.body = body.encode('utf-8')
            self.headers.update({"Content-Length": str(len(self.body))})
        else:
            self.body = body
