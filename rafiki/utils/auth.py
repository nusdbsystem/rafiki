import os
import jwt
from functools import wraps
from datetime import datetime, timedelta

from rafiki.constants import UserType
from rafiki.config import APP_SECRET, SUPERADMIN_EMAIL

TOKEN_EXPIRATION_HOURS = 1

class UnauthorizedError(Exception): pass
class InvalidAuthorizationHeaderError(Exception): pass
    
def generate_token(user):
    payload = {
        'user_id': user['id'],
        'user_type': user['user_type'],
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS)
    }
    token = jwt.encode(payload, APP_SECRET, algorithm='HS256')
    return token.decode('utf-8')

def decode_token(token):
    payload = jwt.decode(token, APP_SECRET, algorithms=['HS256'])
    return payload

def auth(user_types=[]):
    from flask import request
    
    user_types.append(UserType.SUPERADMIN)

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            auth_header = request.headers.get('authorization', None)
            token = extract_token_from_header(auth_header)
            auth = decode_token(token)

            if auth.get('user_type') not in user_types:
                raise UnauthorizedError()

            return f(auth, *args, **kwargs)

        return wrapped
    return decorator

def extract_token_from_header(header):
    if header is None:
        raise InvalidAuthorizationHeaderError()
    
    parts = header.split(' ')
    
    if len(parts) != 2:
        raise InvalidAuthorizationHeaderError()

    if parts[0] != 'Bearer':
        raise InvalidAuthorizationHeaderError()

    token = parts[1]
    return token

def superadmin_client():
    from rafiki.client import Client
    admin_host = os.environ['ADMIN_HOST']
    admin_port = os.environ['ADMIN_PORT']
    client = Client(admin_host=admin_host, 
                    admin_port=admin_port)
    client.login(email=SUPERADMIN_EMAIL, password=os.environ['SUPERADMIN_PASSWORD'])
    return client
