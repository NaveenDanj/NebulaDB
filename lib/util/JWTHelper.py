import datetime
import jwt
import os


def encode_auth_token(payload):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp':
            datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat':
            datetime.datetime.utcnow(),
            'sub':
            'test'
        }
        return jwt.encode(payload, os.getenv("SECRET"), algorithm='HS256')
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, os.getenv("SECRET"))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'