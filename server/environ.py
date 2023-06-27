from .http_request import RequestLineHeadersParse


class Environ:

    def __init__(self, request: bytes):
        self._raw_request = RequestLineHeadersParse(request)
        self._environ = dict()

    def _from_start_line_to_environ(self) -> None:
        self._environ.update({
            k: v for (k, v) in zip(('REQUEST_METHOD', 'PATH_INFO', 'QUERY_STRING', 'PROTOCOL'),
                                   self._raw_request.parse_starline())
        })

    def _from_headers_to_environ(self) -> None:
        self._environ.update(self._raw_request.parse_headers())

    def get_environ(self) -> dict:
        self._from_start_line_to_environ()
        self._from_headers_to_environ()
        return self._environ
