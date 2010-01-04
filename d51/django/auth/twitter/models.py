from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class TwitterToken(models.Model):
    uid = models.PositiveIntegerField(primary_key=True)
    user = models.OneToOneField(User, related_name='twitter')
    key = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)
