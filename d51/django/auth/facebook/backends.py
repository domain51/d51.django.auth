from d51.django.auth.facebook.models import FacebookID
from django.contrib.auth.models import User

FACEBOOK_CONNECT_BACKEND_STRING = 'd51.django.auth.facebook.backends.FacebookConnectBackend'

class FacebookConnectBackend(object):
    def __init__(self, manager=FacebookID.objects, user_manager=User.objects):
        self.manager = manager
        self.user_manager = user_manager

    def authenticate(self, **kwargs):
        if not 'request' in kwargs:
            return

        request = kwargs['request']
        if not request.facebook.check_session(request):
            return

        try:
            user = self.manager.get_uid(request.facebook.uid).user
        except self.manager.model.DoesNotExist:
            user = request.user.is_authenticated() and request.user or self._create_new_user(request)
            fb_id = self.manager.create(pk=request.facebook.uid, user=user)

        user.backend = FACEBOOK_CONNECT_BACKEND_STRING
        return user

    def _create_new_user(self, request):
        user_info = request.facebook.users.getInfo([request.facebook.uid], ['name'])[0]
        user_name = user_info['name'].split(' ')
        user = self.user_manager.create(
            username='fb$%d' % request.facebook.uid,
            first_name=user_name[0],
            last_name=user_name[1]
        )
        user.set_unusable_password()
        user.save()
        return user

    # TODO: this should be in a generic super-class
    def get_user(self, user_id):
        try:
            return self.user_manager.get(pk=user_id)
        except self.user_manager.model.DoesNotExist:
            return None

