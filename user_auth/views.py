from django.shortcuts import render
import jwt
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserInfo
import json 
from django.contrib.auth import authenticate
KEY = "qwerqwqwefknskacnfjbnjvgjeriuyweoLKUHHLKJEfhkerjnfkjrw1lklk~~~fesfdcvse"
# Create your views here.

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username', None)
        password = data.get('password', None)
        email = data.get('email', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            return HttpResponse('Wrong request')

        user = User.objects.create_user(username, email, password)
        user.save()

        user_info = UserInfo(user=user)
        user_info.save()

        encoded = jwt.encode({'username': user.username, 'password': password}, KEY, algorithm="HS256")

        return JsonResponse({"username": user.username, "token": encoded, 'is_admin': user_info.is_admin, 'is_editor': user_info.is_editor}, safe=False)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse('Wrong request')

        encoded = jwt.encode({'username': user.username, 'password': password}, KEY, algorithm="HS256")
        user_info = UserInfo.objects.filter(user=user).first()
        return JsonResponse({"username": user.username, "token": encoded, 'is_admin': user_info.is_admin, 'is_editor': user_info.is_editor}, safe=False)

def authenticate_user(token):
    if len(token) == 0:
        return None
    print(token)
    user_dict = jwt.decode(token, KEY, algorithms=["HS256"])
    username = user_dict.get('username', None)
    password = user_dict.get('password', None)
    user = authenticate(username=username, password=password)
    if user is None:
        return None
    user_info = UserInfo.objects.filter(user=user).first()
    return user_info

def getUsers(request):
    if request.method == 'GET':
        token = request.headers.get('Token', None)
        print("\n\n\n\n",token,"\n\n\n")
        if token is None:
            return HttpResponse(status=401)
        user = authenticate_user(token)
        if user is None:
            return HttpResponse(status=401)
        if user.is_admin == False:
            return HttpResponse(status=401)

        users = UserInfo.objects.all()
        result = []
        for u in users:
            temp = model_to_dict(u)
            temp['email'] = u.user.email
            temp['username'] = u.user.username
            result.append(temp)
        return JsonResponse(result, safe=False)
    return HttpResponse(status=405)

@csrf_exempt
def setUserPermissions(request):
    if request.method == 'POST':


        token = request.headers.get('Token', None)
        if token is None:
            return HttpResponse(status=401)
        user = authenticate_user(token)
        if user is None:
            return HttpResponse(status=401)
        if user.is_admin == False:
            return HttpResponse(status=401)

        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id', None)
        is_admin = data.get('is_admin', None)
        is_editor = data.get('is_editor', None)

        new_user = UserInfo.objects.get(pk=user_id)
        new_user.is_admin = is_admin
        new_user.is_editor = is_editor
        new_user.save()

        result = model_to_dict(new_user)
        result['email'] = new_user.user.email
        result['username'] = new_user.user.username

        return JsonResponse(result, safe=False)
    return HttpResponse(status=405)



