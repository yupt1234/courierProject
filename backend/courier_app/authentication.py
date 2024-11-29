import jwt, datetime
from rest_framework import exceptions

def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }, 'access_secrete', algorithm='HS256')

def create_refresh_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }, 'refresh_secrete', algorithm='HS256')

def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secrete', algorithms='HS256')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secrete', algorithms='HS256')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')
