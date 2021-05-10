from django.contrib import admin

from django.db import models
from .models import Resource


class ResourceAdmin(admin.ModelAdmin):
    model = Resource

admin.site.register(Resource, ResourceAdmin)