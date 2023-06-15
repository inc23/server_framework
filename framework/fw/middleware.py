from urllib.parse import parse_qs
from uuid import uuid4
from .request import Request
from .response import Response


class Middleware:

    def to_response(self, response: Response):
        pass

    def to_request(self, request: Request):
        pass


class Session(Middleware):

    def to_response(self, response: Response) -> None:
        if not response.request.session_id:
            response.headers.update(
                {'Set-Cookie': f'session_id={uuid4()}'}
            )

    def to_request(self, request: Request) -> None:
        cookies = request.environ.get('COOKIE')
        if not cookies:
            return
        session_id = parse_qs(cookies)['session_id']
        request.extra['session_id'] = session_id


middlewares = [Session]
