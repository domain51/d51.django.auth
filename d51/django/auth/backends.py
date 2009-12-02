from django.contrib.auth.models import User

class AbstractModelAuthBackend(object):
    def __init__(self, user_manager=User.objects, **kwargs):
        self.user_manager = user_manager

    def get_user(self, user_id):
        try:
            return self.user_manager.get(pk=user_id)
        except self.user_manager.model.DoesNotExist:
            return None

