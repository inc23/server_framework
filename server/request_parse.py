import socket
import io
from server.environ import Environ


class RequestParser:

    def __init__(self, client_socket: socket.socket, http_request: bytes):
        self._environ = dict()
        self._client_socket = client_socket
        self._first_part_request = http_request
        self._other_part_request = b''
        self._line_headers = None

    def _build_line_headers(self) -> None:
        while True:
            split_request = self._first_part_request.split(b'\r\n\r\n', maxsplit=1)
            if len(split_request) == 1:
                more = self._client_socket.recv(1024)
                self._first_part_request += more
            else:
                self._line_headers, self._other_part_request = split_request
                break

    def _build_environ(self) -> None:
        self._environ = Environ(self._line_headers).get_environ()
        while len(self._other_part_request) < int(self._environ.get('CONTENT_LENGTH', 0)):
            more = self._client_socket.recv(1024)
            self._other_part_request += more
        self._environ['wsgi.input'] = io.BytesIO(self._other_part_request)

    def get_environ(self) -> dict:
        self._build_line_headers()
        self._build_environ()
        return self._environ



