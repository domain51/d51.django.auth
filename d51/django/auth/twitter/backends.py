from d51.django.auth.backends import AbstractModelAuthBackend 
from d51.django.auth.twitter import utils
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from .models import TwitterToken
from .utils import TWITTER_SESSION_KEY, get_twitter_api, create_new_user, get_http_client

TWITTER_BACKEND_STRING = 'd51.django.auth.facebook.backends.TwitterBackend'

class TwitterBackend(AbstractModelAuthBackend):
    def __init__(self, manager=TwitterToken.objects, settings=django_settings, *args, **kwargs):
        self.manager = manager
        super(TwitterBackend, self).__init__(*args, **kwargs)

    def authenticate(self, **credentials):
        request = credentials.get('request', None)
        if request is None:
            return

        user = None
        self.setup_api_and_token(request)
        user = self.get_twitter_user()
        return user

    def get_http(self, consumer=None, token=None):
        return get_twitter_http(consumer=consumer, token=token)
    
    def get_api(self, consumer=None, token=None):
        return get_twitter_api(consumer=consumer, token=token)

    def get_request_token(self, request):
        request_token = request.session.get(TWITTER_SESSION_KEY, None)
        return request_token

    def fetch_access_token(self, request):
        return utils.fetch_access_token(get_request_token(request), request.GET['oauth_token'])

    def setup_api_and_token(self, request, consumer=None, token=None):
        request_token = self.get_request_token(request)
        self.api, self.token = self.get_api(consumer=consumer, token=token), token    

    def get_twitter_user(self):
        user_info = self.api.account.verify_credentials()
        twitter_token = None
        try:
            twitter_token = self.manager.get_uid(user_info['id'])
            twitter_token.update_from_oauth_token(self.token)
        except TwitterToken.DoesNotExist:
            user = create_new_user(user_info['id'], user_info['name'], user_manager=self.user_manager)
            twitter_token = self.manager.create_new_twitter_token(user, user_info['id'], self.token)
        return twitter_token.user
