from framework.auth.security import verify_password
from framework.auth.jwt import header_jwt, create_jwt_token
from framework.fw.request import Request
from framework.settings import user_model as User


def authenticate(email: str, password: str) -> User | None:
    user = User.objects.get(User.email == email)
    if user:
        if verify_password(password, user.password):
            return user
    return None


def login(request: Request, user: User) -> None:
    payload_jwt = {
        'id': user.id,
        'name': f'{user}',
        'admin': user.is_admin
    }
    jwt = create_jwt_token(header_jwt, payload_jwt)
    request.extra['jwt'] = jwt
