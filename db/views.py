from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db.models import Q
from .driver.onthology_driver import Onthology

uri = 'bolt://infra.iis.nsk.su'
user="neo4j"
password="pupil-flute-lunch-quarter-symbol-1816"


def getClasses(request):
    if request.method == "GET":
        o = Onthology(uri,user, password)
        res = o.getParentClasses('')
        result = []
        for node in res:
            result.append(o.nodeToDict(node))
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


def getClassObjects(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        if id is None:
            return HttpResponse(status=404)
        o = Onthology(uri,user, password)
        res = o.getClassObjects(id)
        result = []
        for node in res:
            result.append(o.nodeToDict(node))
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')

def getSubClasses(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        if id is None:
            return HttpResponse(status=404)
        o = Onthology(uri,user, password)
        res = o.getSubClassesById(id)
        result = []
        for node in res:
            result.append(o.nodeToDict(node))
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')


