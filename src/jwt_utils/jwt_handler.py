import time
import jwt

from src.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_TIME_SECONDS


def token_response(token: str) -> dict[str, str]:

    return {
        'access_token': token
    }


def sign_jwt(user_email: str) -> dict[str, str]:
    payload = {
        'email': user_email,
        'expires': time.time() + JWT_EXPIRATION_TIME_SECONDS,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    token = token.decode('utf-8')
    return token_response(token)


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}
