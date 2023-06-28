import socket
import selectors
import traceback
from time import time
from typing import Callable
from .http_response import Response
from .request_parse import RequestParser


class Server:

    def __init__(self, framework: Callable = None, host: str = 'localhost', port: int = 5000):
        self._selector = selectors.DefaultSelector()
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket, self._addr = None, None
        self._framework = framework
        self._host = host
        self._port = port
        self._run_server()
        self._run_event_loop()

    def _run_server(self) -> None:
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        self._selector.register(self._server_socket, selectors.EVENT_READ, self._accept_connection)

    def _accept_connection(self) -> None:
        if self._client_socket is not None:
            self._client_socket.close()
            self._selector.unregister(self._client_socket)
        self._client_socket, self._addr = self._server_socket.accept()
        print(f'connect with {self._addr}')
        self._selector.register(self._client_socket, selectors.EVENT_READ, self._send_response)

    def _send_response(self) -> None:
        try:
            request = self._client_socket.recv(1024)
            if request:
                t1 = time()
                if self._framework is not None:
                    resp = Response()
                    environ = RequestParser(self._client_socket, request).get_environ()
                    body = self._framework(environ, resp.start_response)
                    response = resp.create_response(body=body)
                else:
                    response = '404'.encode('utf-8')
                self._client_socket.send(response)
                timeout = (time() - t1)*1000
                print(f'timeout time msec {timeout}')

        except Exception:
            traceback.print_exc()

        finally:
            self._selector.unregister(self._client_socket)
            self._client_socket.close()
            self._client_socket = None

    def _run_event_loop(self) -> None:
        while True:
            events = self._selector.select()
            try:
                for event, _ in events:
                    callback = event.data
                    callback()
            except Exception:
                traceback.print_exc()
                continue
