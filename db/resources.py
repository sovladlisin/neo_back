from time import time
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db.models import Q

from core.settings import *
from .onthology_driver import Onthology
from.onthology_namespace import *
from django.http import JsonResponse




# API IMPORTS
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

@api_view(['GET', ])
@permission_classes((AllowAny,))
def getAllResources(request):
    o = Onthology(DB_URI,DB_USER, DB_PASSWORD)
    res = o.getResources()
    
    return JsonResponse(res, safe=False)

@api_view(['GET', ])
@permission_classes((AllowAny,))
def getCorpusResources(request):
    c_uri = request.GET.get('corpus_uri', '')
    res_types = request.GET.get('res_types', [''])
    text_search = request.GET.get('text_search', '')
    lang_id = request.GET.get('lang_id', -1)
    actor_id = request.GET.get('actor_id', -1)
    place_id = request.GET.get('place_id', -1)
    time_search = request.GET.get('time_search', '')
    chunk_number = request.GET.get('chunk_number', 1)
    chunk_size = request.GET.get('chunk_size', 50)
    o = Onthology(DB_URI,DB_USER, DB_PASSWORD)



    res,data_size = o.getCorpusResources(c_uri, res_types, text_search, lang_id, actor_id, place_id, time_search, chunk_number, chunk_size)
    return JsonResponse({'data': res, 'data_size': data_size}, safe=False)

@api_view(['POST', ])
@permission_classes((AllowAny,))
def createEvent(request):
    data = json.loads(request.body.decode('utf-8'))
    actor_id = data.get('actor_id', None)
    place_id = data.get('place_id', None)
    time_string = data.get('time_string', None)
    label = data.get('label', None)

    if None in [actor_id, place_id, time_string,label]:
        return HttpResponse(status=403)


    o = Onthology(DB_URI,DB_USER, DB_PASSWORD)
    res = o.createEvent(actor_id, place_id, time_string,label)
    return HttpResponse(status=200)

