from django.urls import path
from django.conf.urls import url
from .views import addEntity, getClasses,getClassObjects, getSubClasses, updateEntity,getClassObject,addClassAttribute, getClass,getClassesWithSignatures, getObjectsByClassUri
from .corpuses import getCorpuses, getSubCorpuses
from .files import uploadFile,getFiles,deleteFile

urlpatterns = [
    path('getClasses',getClasses , name='getClasses'),
    path('getClassObjects',getClassObjects , name='getClassObjects'),
    path('getSubClasses',getSubClasses , name='getSubClasses'),
    path('updateEntity',updateEntity , name='updateEntity'),
    path('addEntity',addEntity , name='addEntity'),
    path('getClassObject',getClassObject , name='getClassObject'),
    path('addClassAttribute',addClassAttribute , name='addClassAttribute'),
    path('getClass',getClass , name='getClass'),
    path('getCorpuses',getCorpuses , name='getCorpuses'),
    path('getSubCorpuses',getSubCorpuses , name='getSubCorpuses'),
    path('getClassesWithSignatures',getClassesWithSignatures , name='getClassesWithSignatures'),
    path('getObjectsByClassUri',getObjectsByClassUri , name='getObjectsByClassUri'),

    path('uploadFile',uploadFile , name='uploadFile'),
    path('getFiles',getFiles , name='getFiles'),
    path('deleteFile',deleteFile , name='deleteFile'),
]