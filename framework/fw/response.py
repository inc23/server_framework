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
        self._set_body(body)

    def _set_headers(self):
        self.headers.update({
            'Content-Type': "text/html; charset=utf-8",
            "Content-Length": 0
        })

    def _set_body(self, body):
        self.body = body.encode('utf-8')
        self.headers.update({"Content-Length": str(len(self.body))})
