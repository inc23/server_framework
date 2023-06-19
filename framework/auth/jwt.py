import json
import base64
import hmac
import hashlib
from framework.settings import secret_JWT

header_jwt = {
    'alg': 'HS256',
    'typ': 'JWT'
}


def signature_encode(header: bytes | str, payload: bytes | str) -> str:
    secret = secret_JWT
    if isinstance(header, bytes):
        to_sign = f'{header.decode()}.{payload.decode()}'
    else:
        to_sign = f'{header}.{payload}'
    signature = base64.urlsafe_b64encode(
        hmac.new(
            secret.encode(),
            to_sign.encode(),
            hashlib.sha256).digest()).rstrip(b'=')
    return signature.decode()


def create_jwt_token(header: dict, payload: dict) -> str:
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=')
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=')
    signature = signature_encode(header_encoded, payload_encoded)
    jwt = f'{header_encoded.decode()}.{payload_encoded.decode()}.{signature}'
    return jwt


def check_jwt(received_jwt: str) -> dict | bool:

    header_encoded, payload_encoded, signature = received_jwt.split('.')
    new_signature = signature_encode(header_encoded, payload_encoded)
    if new_signature == signature:
        payload_decoded = base64.urlsafe_b64decode(payload_encoded + '==')
        payload = json.loads(payload_decoded.decode())
        return payload
    return False
