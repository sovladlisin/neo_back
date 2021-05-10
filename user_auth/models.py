from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=True)
    is_editor = models.BooleanField(default=True)

