import socket
import selectors
import traceback
from typing import Callable
from .environ import Environ
from .http_response import Response


class Server:

    def __init__(self, framework: Callable = None, host: str = 'localhost', port: int = 5000):
        self.selector = selectors.DefaultSelector()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket, self.addr = None, None
        self.framework = framework
        self.host = host
        self.port = port
        self.run_server()
        self.run_event_loop()

    def run_server(self) -> None:
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.selector.register(self.server_socket, selectors.EVENT_READ, self.accept_connection)

    def accept_connection(self) -> None:
        if self.client_socket is not None:
            self.client_socket.close()
            self.selector.unregister(self.client_socket)
        self.client_socket, self.addr = self.server_socket.accept()
        print(f'connect with {self.addr}')
        self.selector.register(self.client_socket, selectors.EVENT_READ, self.send_response)

    def send_response(self) -> None:
        try:
            request = self.client_socket.recv(1094)
            if request:
                if self.framework is not None:
                    resp = Response()
                    environ = Environ(request).get_environ()
                    body = self.framework(environ, resp.start_response)
                    response = resp.create_response(body=body)
                else:
                    response = '404'.encode('utf-8')
                self.client_socket.send(response)

        except Exception:
            traceback.print_exc()

        finally:
            self.selector.unregister(self.client_socket)
            self.client_socket.close()
            self.client_socket = None

    def run_event_loop(self) -> None:
        while True:
            events = self.selector.select()
            try:
                for event, _ in events:
                    callback = event.data
                    callback()
            except Exception:
                traceback.print_exc()
                continue

