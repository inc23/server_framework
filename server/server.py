import socket
from typing import Generator
import selectors
import traceback
from time import time, sleep
from typing import Callable
from .http_response import Response
from .request_parse import RequestParser
import settings


class Server:

    def __init__(self, framework: Callable = None):
        self._selector = selectors.DefaultSelector()
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._framework = framework
        self._host = settings.host
        self._port = settings.port
        self._run_server()
        self._run_event_loop()

    def _run_server(self) -> None:
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        self._selector.register(self._server_socket, selectors.EVENT_READ, (self._accept_connection, self._server_socket))
        print(f'server start at http://{self._host}:{self._port}')

    def _accept_connection(self, sock) -> None:
        client_socket, addr = sock.accept()
        print(f'connect with {addr}')
        self._selector.register(client_socket, selectors.EVENT_READ, (self._send_response, client_socket))

    def _send_response(self, sock) -> None:
        try:
            request = sock.recv(1024)
            if request:
                t1 = time()
                resp = Response()
                environ = RequestParser(sock, request).get_environ()
                body = self._framework(environ, resp.start_response)
                response = resp.create_response(body=body)
                if isinstance(body, Generator):
                    sock.sendall(response)
                    for item in body:
                        sock.sendall(item)
                else:
                    sock.sendall(response)
                timeout = (time() - t1) * 1000
                print(f'timeout time msec {timeout}')

        except Exception:
            traceback.print_exc()

        finally:
            self._selector.unregister(sock)
            sock.close()

    def _run_event_loop(self) -> None:
        while True:
            events = self._selector.select()
            try:
                for key, _ in events:
                    callback, sock = key.data
                    callback(sock)
            except Exception:
                traceback.print_exc()
                continue
