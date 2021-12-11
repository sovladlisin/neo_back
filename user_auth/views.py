import jwt
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token

import json 
KEY = "qwerqwqwefknskacnfjbnjvgjeriuyweoLKUHHLKJEfhkerjnfkjrw1lklk~~~fesfdcvse"
# Create your views here.

# API IMPORTS
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import LoginSerializer, RegistrationSerializer

@api_view(['POST', ])
@permission_classes((AllowAny,))
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data = collect_account_func(account)

        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST', ])
@permission_classes((AllowAny,))
def login_view(request):

    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.authenticate()
            data = collect_account_func(account)

        else:
            print('valid error')
            data = serializer.errors
        return Response(data)




def collect_account_func(account):
    data = {}
    data['response'] = 'Success'
    data['email'] = account.email
    data['username'] = account.email
    token = Token.objects.get(user=account).key
    data['token'] = token
    data['is_admin'] = account.is_admin
    data['id'] = account.pk
    return data
