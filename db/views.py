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
from user_auth.views import authenticate_user

uri = 'bolt://infra.iis.nsk.su'
user="neo4j"
password="pupil-flute-lunch-quarter-symbol-1816"


def getClasses(request):
    if request.method == "GET":
        print(request.headers.get('Token', None))
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

def getClassObject(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        if id is None:
            return HttpResponse(status=404)
        o = Onthology(uri,user, password)

        node, signature, attributes, attributes_obj = o.getClassObject(id)

        obj = o.nodeToDict(node)

        attrs = []
        attrs_obj = []
        for a in attributes:
            attrs.append(o.nodeToDict(a))
        for a in attributes_obj:
            attrs_obj.append(o.relToDict(a))

        return JsonResponse({'object': obj, 'class_signature': signature, 'class_attributes': attrs, 'relations': attrs_obj }, safe=False)
    return HttpResponse('Wrong request')

def getClass(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        if id is None:
            return HttpResponse(status=404)
        o = Onthology(uri,user, password)
        class_node, attributes, objects, attr_types, attributes_obj, attributes_types_obj = o.getClassById(id)
        class_obj = o.nodeToDict(class_node)
        attrs = []
        objs = []
        types = {}
        attrs_obj = []
        types_attr = {}

        for a in attributes:
            attrs.append(o.nodeToDict(a))
        for a in attributes_obj:
            attrs_obj.append(o.nodeToDict(a))

        for obj in objects:
            objs.append(o.nodeToDict(obj))

        for a_t in attr_types:
            types[a_t] = o.nodeToDict(attr_types[a_t])
        for a_t in attributes_types_obj:
            types_attr[a_t] = o.nodeToDict(attributes_types_obj[a_t])

        
        return JsonResponse({'class': class_obj, 'attributes': attrs, 'objects': objs, 'types': types, 'attributes_obj':attrs_obj ,'attribute_types':types_attr}, safe=False)
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

def addClassAttribute(request):
    if request.method == "GET":
        o = Onthology(uri,user, password)
        o.addClassAttribute(27, STRING, 'test@en,тест@ru', PROPERTY_URI + 'test')
        return HttpResponse('Wrong request')

def getClassesWithSignatures(request):
    if request.method == "GET":
        o = Onthology(uri,user, password)
        res = o.getClassesWithSignatures()
        result = []
        for r in res:
            result.append(o.nodeToDict(r))
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')

def getObjectsByClassUri(request):
    if request.method == "GET":
        uri_s = request.GET.get('uri', None)
        if uri is None:
            return HttpResponse(status=404)

        o = Onthology(uri,user, password)
        res = o.getObjectsByClassUri(uri_s)
        result = []
        for r in res:
            result.append(o.nodeToDict(r))
        return JsonResponse(result, safe=False)
    return HttpResponse('Wrong request')

@csrf_exempt
def updateEntity(request):
    if request.method == 'POST':

        token = request.headers.get('Token', None)
        if token is None:
            return HttpResponse(status=401)
        user = authenticate_user(token)
        if user is None:
            return HttpResponse(status=401)
        if user.is_editor == False:
            return HttpResponse(status=401)

        data = json.loads(request.body.decode('utf-8'))
        o = Onthology(uri,user, password)
        node = o.updateEntity(data)
        return JsonResponse(o.nodeToDict(node), safe=False)
    return HttpResponse('Wrong request')

@csrf_exempt
def addEntity(request):
    if request.method == 'POST':

        token = request.headers.get('Token', None)
        if token is None:
            return HttpResponse(status=401)
        user = authenticate_user(token)
        if user is None:
            return HttpResponse(status=401)
        if user.is_editor == False:
            return HttpResponse(status=401)


        data = json.loads(request.body.decode('utf-8'))
        labels = data['labels']
        node = data['node']
        o = Onthology(uri,user, password)
        created_node = o.createEntity(labels, node)
        print('IDIDIDIDIDI:', created_node.id)
        return JsonResponse(o.nodeToDict(created_node), safe=False)
    return HttpResponse('Wrong request')

@csrf_exempt
def deleteEntity(request):
    if request.method == 'DELETE':

        token = request.headers.get('Token', None)
        if token is None:
            return HttpResponse(status=401)
        user = authenticate_user(token)
        if user is None:
            return HttpResponse(status=401)
        if user.is_editor == False:
            return HttpResponse(status=401)

            
        id = request.DELETE.get('id', None)
        if id is None:
            return HttpResponse(status=404)

        o = Onthology(uri,user, password)
        node = o.deleteEntity(id)
        return JsonResponse({"result": True}, safe=False)
    return HttpResponse('Wrong request')