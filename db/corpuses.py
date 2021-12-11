from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db.models import Q
from .onthology_driver import Onthology
from.onthology_namespace import *


uri = 'bolt://infra.iis.nsk.su'
user="neo4j"
password="pupil-flute-lunch-quarter-symbol-1816"


# API IMPORTS
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['GET', ])
@permission_classes((AllowAny,))
def getCorpuses(request):
    o = Onthology(uri,user, password)
    res = o.getCorpuses()
    
    return JsonResponse(res, safe=False)


@api_view(['GET', ])
@permission_classes((AllowAny,))
def getSubCorpuses(request):
    id = request.GET.get('id', None)
    if id is None:
        return HttpResponse(status=404)

    o = Onthology(uri,user, password)
    res = o.getSubCorpuses(id)
    result = []
    for node in res:
        result.append(o.nodeToDict(node))
    return JsonResponse(result, safe=False)
