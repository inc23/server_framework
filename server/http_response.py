from typing import List, Tuple
import http


class Response:

    def __init__(self):
        self._status_code = None
        self._headers = None
        self._start_line = None

    def start_response(self, status_code: int = 200, headers: List[Tuple[str, str]] = None) -> None:
        code = str(status_code).encode('utf-8')
        status = http.HTTPStatus(status_code).phrase.encode()
        self._start_line = b'HTTP/1.1 ' + code + b' ' + status + b'\r\n'
        headers_list = [k.encode('utf-8') + b': ' + v.encode('utf-8') + b'\r\n' for k, v in headers]
        headers_list.append(b'Connection: close\r\n')
        self._headers = b''.join(headers_list)

    def create_response(self, body: bytes = b'') -> bytes:
        content = [self._start_line, self._headers, b'\r\n' if body else b'', body]
        return b''.join(content)

