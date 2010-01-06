from d51.django.auth.backends import AbstractModelAuthBackend 
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from .models import TwitterToken
from .utils import TWITTER_SESSION_KEY, get_twitter_http, get_twitter_api, create_new_user

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
        try:
            self.setup_api_and_token(request)
            user = self.get_twitter_user()
        except Exception as e:
            user = None 
        return user

    def get_http(self):
        return get_twitter_http()
    
    def get_api(self, authorized_http):
        return get_twitter_api(authorized_http)

    def get_request_token(self, request):
        request_token = request.session.get(TWITTER_SESSION_KEY, None)
        return request_token

    def authorize_http(self, http, request_token):
        http.token = request_token
        access_token = http.fetch_access_token()
        http.token = access_token
        return http

    def setup_api_and_token(self, request):
        request_token = self.get_request_token(request)
        http = self.get_http()
        http = self.authorize_http(http, request_token)
        self.api, self.token = self.get_api(http), http.token    

    def get_twitter_user(self):
        user_info = self.api.account.verify_credentials()
        twitter_token = None
        try:
            twitter_token = self.manager.get_uid(user_info['id'])
            twitter_token.update_from_oauth_token(self.token)
        except TwitterToken.DoesNotExist:
            user = create_new_user(user_manager=self.user_manager, **user_info)
            twitter_token = self.manager.create_new_twitter_token(user, user_info['id'], self.token)
        return twitter_token.user
