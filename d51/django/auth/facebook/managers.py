from django.db import models

class FacebookIDManager(models.Manager):
    def get_uid(self, uid):
        return self.get(pk = uid)

