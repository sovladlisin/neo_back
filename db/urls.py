from django.urls import path
from django.conf.urls import url
from .views import deleteOntology, searchIndex, updateIndex, getClassFullSignature, addEntity, getDomainOntologies, getAllClasses, getClasses,getClassObjects, addClassAttributeObject, updateEntity, getSubClasses, updateEntity,getClassObject,addClassAttribute, getClass,getClassesWithSignatures, getObjectsByClassUri
from .corpuses import getCorpuses, getSubCorpuses
from .files import changeComments,uploadFile,getFiles,deleteFile
from .workspace import deleteMarkup, getTextEntities, getWorkspace,getMarkups,addMarkup, deleteTextEntity, createTextEntity, editMarkup,getNodeAttributes, createTextRelation, getTextRelations, deleteTextRelation
from .resources import (
    getAllResources
)
urlpatterns = [
    path('getDomainOntologies',getDomainOntologies , name='getDomainOntologies'),
    path('deleteOntology',deleteOntology , name='deleteOntology'),

    path('getClasses',getClasses , name='getClasses'),
    path('getAllClasses',getAllClasses , name='getAllClasses'),
    path('getClassObjects',getClassObjects , name='getClassObjects'),
    path('getSubClasses',getSubClasses, name='getSubClasses'),

    path('getAllResources',getAllResources, name='getAllResources'),


    path('updateEntity',updateEntity , name='updateEntity'),
    path('addEntity',addEntity , name='addEntity'),


    path('getClassObject',getClassObject , name='getClassObject'),

    path('addClassAttribute',addClassAttribute , name='addClassAttribute'),
    path('addClassAttributeObject',addClassAttributeObject , name='addClassAttributeObject'),


    path('getClass',getClass , name='getClass'),
    path('getCorpuses',getCorpuses , name='getCorpuses'),
    path('getSubCorpuses',getSubCorpuses , name='getSubCorpuses'),
    path('getClassesWithSignatures',getClassesWithSignatures , name='getClassesWithSignatures'),
    path('getObjectsByClassUri',getObjectsByClassUri , name='getObjectsByClassUri'),

    path('uploadFile',uploadFile , name='uploadFile'),
    path('getFiles',getFiles , name='getFiles'),
    path('deleteFile',deleteFile , name='deleteFile'),
    path('changeComments',changeComments , name='changeComments'),

    path('getWorkspace',getWorkspace , name='getWorkspace'),

    path('getMarkups',getMarkups , name='getMarkups'),
    path('addMarkup',addMarkup , name='addMarkup'),
    path('editMarkup',editMarkup , name='editMarkup'),
    path('deleteMarkup',deleteMarkup , name='deleteMarkup'),

    path('getTextEntities',getTextEntities , name='getTextEntities'),
    path('createTextEntity',createTextEntity , name='createTextEntity'),
    path('deleteTextEntity',deleteTextEntity , name='deleteTextEntity'),

    path('getNodeAttributes',getNodeAttributes , name='getNodeAttributes'),

    path('createTextRelation',createTextRelation , name='createTextRelation'),
    path('getTextRelations',getTextRelations , name='getTextRelations'),
    path('deleteTextRelation',deleteTextRelation , name='deleteTextRelation'),

    path('getClassFullSignature',getClassFullSignature , name='getClassFullSignature'),

    path('updateIndex',updateIndex , name='updateIndex'),
    path('searchIndex',searchIndex , name='searchIndex'),


]