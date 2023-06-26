import socket
import io
import cgi


class MultiPartParser:

    def __init__(self, environ: dict, client_socket: socket.socket, http_request: bytes):
        self.environ = environ
        self.client_socket = client_socket
        self.http_request = http_request
        self.parts_data = b''
        self._build_data()

    def _build_data(self) -> None:
        while len(self.parts_data) < int(self.environ.get('CONTENT_LENGTH')):
            more = self.client_socket.recv(1024)
            self.parts_data += more
        self.environ['wsgi.input'] = io.BytesIO(self.parts_data)




