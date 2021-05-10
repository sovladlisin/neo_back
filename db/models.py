from django.db import models

class File(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

class Resource(models.Model):
    source = models.FileField(upload_to='db.File/bytes/filename/mimetype', blank=True, null=True)
    name = models.CharField(default='Не указано', max_length=500)