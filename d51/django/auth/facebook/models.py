from d51.django.auth.facebook.managers import FacebookIDManager
from django.contrib.auth.models import User
from django.db import models

class FacebookID(models.Model):
    user = models.OneToOneField(User, related_name="facebook")

    objects = FacebookIDManager()

