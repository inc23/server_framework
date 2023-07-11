import secrets
from urllib.parse import parse_qs
from .request import Request
from .response import Response
from framework.auth.jwt import check_jwt
import user_settings


class Middleware:

    def to_response(self, response: Response):
        pass

    def to_request(self, request: Request):
        pass


class JWT(Middleware):

    def to_response(self, response: Response) -> None:
        if response.request.jwt:
            cookies = response.request.environ.get('COOKIE')
            if not parse_qs(cookies).get('jwt'):
                response.headers.update(
                    {'Set-Cookie': f'jwt={response.request.jwt}; Max-Age=100; Path=/'}
                )

    def to_request(self, request: Request) -> None:
        cookies = request.environ.get('COOKIE')
        if not cookies:
            return
        jwt = parse_qs(cookies, separator='; ').get('jwt')
        if jwt:
            payload = check_jwt(jwt[0])
            if payload:
                user_id = payload.get('id')
                user = user_settings.user_model
                request.extra['user'] = user.objects.get(user.id == user_id)


class CSRFToken(Middleware):

    def to_response(self, response: Response):
        if response.request.csrf_token:
            cookies = response.request.environ.get('COOKIE')
            if not parse_qs(cookies, separator='; ').get('csrftoken'):
                response.headers.update(
                    {'Set-Cookie': f'csrftoken={response.request.csrf_token};'
                                   f' Max-Age=31449600; Path=/; Secure; SameSite=Lax'}
                )

    def to_request(self, request: Request):
        cookies = request.environ.get('COOKIE')
        csrf = parse_qs(cookies, separator='; ').get('csrftoken')
        if csrf is not None:
            request.extra['csrf_token'] = csrf[0]
        else:
            request.extra['csrf_token'] = secrets.token_hex(16)


middlewares = [JWT, CSRFToken]
