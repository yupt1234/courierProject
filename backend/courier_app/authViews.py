from rest_framework.views import APIView
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from .authentication import *
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from .authentication import decode_access_token

class UserLoginView(APIView):
    def post(self, request):
        
        userObj = User.objects.filter(email = request.data.get('email')).first()

        response = Response()

        if not userObj:
            response.data = {
                'invalid': 'Invalid Email or Password'
            }
            return response
        if not check_password(request.data.get('password'), userObj.password):
            response.data = {
                'invalid': 'Invalid Email or Password'
            }
            return response
        
        access_token = create_access_token(userObj.id)
        refresh_token = create_refresh_token(userObj.id)

        response.set_cookie(key='refreshToken', value=refresh_token)
        
        response.data = {
            'accessToken': access_token,
            'refreshToken': refresh_token,
            'userData': [User.objects.filter(email=request.data.get('email')).values()[0]],
        }
        return response


def authenticate_request(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', '').split(' ')[1]
            if not access_token:
                return Response({'error': 'Access token missing'}, status=401)
            user_id = decode_access_token(access_token)
            request.user_id = user_id
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=401)
    return wrapper