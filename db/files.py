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
from .onthology_driver import Onthology
from.onthology_namespace import *

uri = 'bolt://infra.iis.nsk.su'
user="neo4j"
password="pupil-flute-lunch-quarter-symbol-1816"

@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':

        # token = request.headers.get('Token', None)
        # if token is None:
        #     return HttpResponse(status=401)
        # user_l = authenticate_user(token)
        # if user_l is None:
        #     return HttpResponse(status=401)
        # if user_l.is_admin == False:
        #     return HttpResponse(status=401)


  
        file_d = request.FILES['file']

        name = request.GET.get('name','')
        object_id = request.GET.get('object_id','')
        file_type = request.GET.get('file_type','')

        o = Onthology(uri,user, password)

        object_node = o.getEntityById(object_id)
        object_uri = object_node.get('uri')


        res = Resource()
        res.source.save(file_d.name,  ContentFile(file_d.read()))
        res.name = name
        # res.original_object_uri = object_uri
        res.save()

        o = Onthology(uri,user, password)

        r = o.connectDigitalToResource(file_type, res.id,name,object_node.id )
        res.original_object_uri = object_uri['uri']
        res.save()

        return JsonResponse(o.nodeToDict(r), safe=False)
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

@csrf_exempt
def changeComments(request):
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
        comments = data.get('comments', None)
        commentary_uri = data.get('commentary_uri', None)

        commentary = ContentFile(b'')
        for comment in comments:
            temp = comment['text'] + '\n'
            commentary.write(temp.encode('utf-8'))



        resource_texts = Resource.objects.get(original_object_uri=commentary_uri)
        resource_texts.source.save(
            'commentary_' + str(resource_texts.pk) + '.txt', commentary)
        return HttpResponse(status=200)
    return HttpResponse(status=403)