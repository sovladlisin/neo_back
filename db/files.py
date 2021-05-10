from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db.models import Q
from django.core.files.base import ContentFile
from .models import Resource
from user_auth.views import authenticate_user

@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':

        token = request.headers.get('Token', None)
        if token is None:
            return HttpResponse(status=401)
        user = authenticate_user(token)
        if user is None:
            return HttpResponse(status=401)
        if user.is_admin == False:
            return HttpResponse(status=401)



        file_d = request.FILES['file']
        name = request.GET.get('name','')
        res = Resource()
        res.source.save(file_d.name,  ContentFile(file_d.read()))
        res.name = name
        res.save()

        result = {}
        result['name'] = res.name
        result['source'] = res.source.url
        result['id'] = res.pk

        return JsonResponse(result, safe=False)
    return HttpResponse(status=405)

def getFiles(request):
    if request.method == 'GET':
        result = []
        files = Resource.objects.all()
        for f in files:
            temp = {}
            temp['name'] = f.name
            temp['source'] = f.source.url
            temp['id'] = f.pk
            result.append(temp)

        return JsonResponse(result, safe=False)
    return HttpResponse(status=405)

@csrf_exempt
def deleteFile(request):
    if request.method == 'DELETE':

        token = request.headers.get('Token', None)
        if token is None:
            return HttpResponse(status=401)
        user = authenticate_user(token)
        if user is None:
            return HttpResponse(status=401)
        if user.is_admin == False:
            return HttpResponse(status=401)

        id = request.GET.get('id',None)
        if id is None:
            return HttpResponse(status=403)
        resource = Resource.objects.get(pk=id)
        resource.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=405)
