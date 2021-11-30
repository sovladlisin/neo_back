from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

class Resource(models.Model):
    source = models.FileField(upload_to='db.File/bytes/filename/mimetype', blank=True, null=True)
    name = models.CharField(default='Не указано', max_length=500)
    original_object_uri = models.CharField(default='', max_length=1000)
    resource_type = models.CharField(default='', max_length=300)

class Markup(models.Model):
    user = models.ForeignKey(
        User, blank=False, null=True, related_name='markup_owner', on_delete=models.CASCADE)
    name = models.CharField(default='Не указано', max_length=500)
    original_object_uri = models.CharField(default='', max_length=1000)
    ontology_uri = models.CharField(default='', max_length=1000)


class Entity(models.Model):
    pos_start = models.IntegerField(default=0)
    pos_end = models.IntegerField(default=0)
    node_uri = models.CharField(default='', max_length=1000)
    markup = models.ForeignKey(
        Markup, blank=False, null=True, related_name='entity_markup', on_delete=models.CASCADE)

class TextRelation(models.Model):
    start = models.ForeignKey(
        Entity, blank=False, null=True, related_name='start_entity', on_delete=models.CASCADE)
    end = models.ForeignKey(
        Entity, blank=False, null=True, related_name='end_entity', on_delete=models.CASCADE)
    connection = models.ForeignKey(
        Entity, blank=False, null=True, related_name='connection_entity', on_delete=models.CASCADE)
    markup = models.ForeignKey(
        Markup, blank=False, null=True, related_name='relation_markup', on_delete=models.CASCADE)