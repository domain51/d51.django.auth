from django.db import models
from .utils import create_new_user

class TwitterTokenManager(models.Manager):
    def get_uid(self, uid):
        return self.get(uid=uid)

    def create_new_twitter_token(self, user, id, token):
        return self.create(
            uid=int(id),
            user=user,
            key=token.key,
            secret=token.secret
        )
