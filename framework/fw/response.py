from .request import Request


class Response:

    def __init__(self, request: Request, status_code=200, headers=None, body=''):
        self.request = request
        self.status_code = status_code
        self.headers = dict()
        self.body = b''
        self._set_headers()
        if headers is not None:
            self.headers.update(headers)
        if body:
            self._set_body(body)
        self.extra = dict()

    def __getattr__(self, item):
        return self.extra.get(item)

    def _set_headers(self):
        self.headers.update({
            'Content-type': 'text/html; charset=utf-8',
            "Content-Length": 0
        })

    def _set_body(self, body):
        print(body.encode())
        self.body = body.encode('utf-8')
        self.headers.update({"Content-Length": str(len(self.body))})
