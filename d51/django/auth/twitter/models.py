from django.conf import settings
from django.contrib.auth.models import User
from oauth.oauth import OAuthToken
from django.db import models
from .managers import TwitterTokenManager

class TwitterToken(models.Model):
    uid = models.PositiveIntegerField(primary_key=True)
    user = models.OneToOneField(User, related_name='twitter')
    key = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)

    objects = TwitterTokenManager()

    def get_oauth_token(self):
        return OAuthToken(self.key, self.secret)
