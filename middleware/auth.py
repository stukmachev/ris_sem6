from typing import Optional
import jwt
from werkzeug.wrappers import Response, Request
from .base import Middleware


class AuthorizationMiddle(Middleware):

    def __init__(self,wsgi_app):
        self.wsgi_app=wsgi_app

    def _generate_token(self, request: Request) -> Optional[str]:
        body=request.json
        try:
            if not isinstance(body, dict):
                raise TypeError('Body has invalid type')
            username=body.get('username', '')
            password=body.get('passord', '')
            if username=='admin' and password=='admin':
                user_id='1'
                return self._encode_token(username, password, user_id)
            return None
        except TypeError:
            return None

    def _encode_token(self,username, password, user_id):
        token=jwt.encode(
            payload={
                'username':username,
                'password':password,
                'user_id':user_id
            },
            key='my super key',
            algorithm='HS256'
        )
        return token

    @staticmethod
    def _decode_token(request: Request):
        try:
            token = request.headers.get('Authorization','')
            decoded=jwt.decode(token,key='my super key', algorithm='HS256')['user_id']
            return decoded
        except(KeyError, jwt.exceptions.DecodeError):
            return None

    def __call__(self, environ, start_response):
        print('I am from middleware')
        request=Request(environ)
        if request.path=='/token'and request.method=='POST':
            token=self._generate_token(request)
            if token is None:
                return Response('No such user', status=401)(environ, start_response)
            return Response(token, status=200)(environ, start_response)
        else:
            user_id=self.decode_token(request)
            if user_id:
                environ['HTTP_AUTH_MIDDLEWARE_USER']
        print(request.json)
        return self.wsgi_app(environ, start_response)