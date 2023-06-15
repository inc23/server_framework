from .http_request import RequestParse


class Environ:

    def __init__(self, request: bytes):
        self.raw_request = RequestParse(request)
        self.environ = dict()

    def from_start_line_to_environ(self) -> None:
        self.environ.update({
            k: v for (k, v) in zip(('REQUEST_METHOD', 'PATH_INFO', 'QUERY_STRING', 'PROTOCOL'),
                                   self.raw_request.parse_starline())
        })

    def from_headers_to_environ(self) -> None:
        self.environ.update(self.raw_request.parse_headers())

    def from_body_to_environ(self) -> None:
        self.environ.update({'wsgi_input': self.raw_request.parse_body()})

    def get_environ(self) -> dict:
        self.from_start_line_to_environ()
        self.from_headers_to_environ()
        self.from_body_to_environ()
        return self.environ
