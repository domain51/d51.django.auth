from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from .managers import TwitterTokenManager
import oauth2

class TwitterToken(models.Model):
    uid = models.PositiveIntegerField(primary_key=True)
    user = models.OneToOneField(User, related_name='twitter')
    key = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)

    objects = TwitterTokenManager()

    def get_oauth_token(self):
        return oauth2.Token(self.key, self.secret)

    def update_from_oauth_token(self, token):
        self.key, self.secret = token.key, token.secret
        self.save()
