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
from .onthology_driver import Onthology
from.onthology_namespace import *

uri = 'bolt://infra.iis.nsk.su'
user="neo4j"
password="pupil-flute-lunch-quarter-symbol-1816"

# API IMPORTS
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def uploadFile(request):

 
    file_d = request.FILES['file']

    name = request.GET.get('name','')
    object_id = request.GET.get('object_id','')
    file_type = request.GET.get('file_type','')
    note = request.GET.get('note','')

    o = Onthology(uri,user, password)

    object_node = o.getEntityById(object_id)
    object_uri = object_node.get('uri')


    res = Resource()
    res.source.save(file_d.name,  ContentFile(file_d.read()))
    res.name = name
    res.resource_type = file_type
    # res.original_object_uri = object_uri
    res.save()

    o = Onthology(uri,user, password)

    r = o.connectDigitalToResource(file_type, res.id,name,object_node.id, note )
    res.original_object_uri = r['uri']
    res.save()

    return JsonResponse(o.nodeToDict(r), safe=False)



@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def deleteFile(request):
    id = request.GET.get('id',None)
    if id is None:
        return HttpResponse(status=403)
    resource = Resource.objects.get(pk=id)
    resource.delete()
    return HttpResponse(status=200)

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def changeComments(request):

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