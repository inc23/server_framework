from urllib.parse import parse_qs
from .request import Request
from .response import Response
from framework.auth.jwt import check_jwt
from ..model import User


class Middleware:

    def to_response(self, response: Response):
        pass

    def to_request(self, request: Request):
        pass


# class Session(Middleware):
#
#     def to_response(self, response: Response) -> None:
#         if not response.request.session_id:
#             response.headers.update(
#                 {'Set-Cookie': f'session_id={uuid4()}'}
#             )
#
#     def to_request(self, request: Request) -> None:
#         cookies = request.environ.get('COOKIE')
#         if not cookies:
#             return
#         session_id = parse_qs(cookies)['session_id']
#         request.extra['session_id'] = session_id

class Session(Middleware):

    def to_response(self, response: Response) -> None:
        if response.request.jwt:
            cookies = response.request.environ.get('COOKIE')
            if not parse_qs(cookies).get('jwt'):
                response.headers.update(
                    {'Set-Cookie': f'jwt={response.request.jwt}; Max-Age=10;'}
                )

    def to_request(self, request: Request) -> None:
        cookies = request.environ.get('COOKIE')
        if not cookies:
            return
        jwt = parse_qs(cookies).get('jwt')
        print(jwt)
        if jwt:
            payload = check_jwt(jwt[0])
            if payload:
                user_id = payload.get('id')
                request.extra['user'] = User.objects.get(User.id == user_id)


middlewares = [Session]