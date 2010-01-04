from d51.django.auth.backends import AbstractModelAuthBackend 
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from .models import TwitterToken
from .utils import TWITTER_SESSION_KEY, get_twitter_http, get_twitter_api

TWITTER_BACKEND_STRING = 'd51.django.auth.facebook.backends.TwitterBackend'

class TwitterBackend(AbstractModelAuthBackend):
    def __init__(self, manager=TwitterToken.objects, settings=django_settings, *args, **kwargs):
        self.manager = manager
        super(TwitterBackend, self).__init__(*args, **kwargs)

    def authenticate(self, **credentials):
        request = credentials.get('request', None)
        if request is None:
            return

        self.setup_api_and_token(request)
        if self.api is None:
            return

        # guard against anything bubbling up through Dolt
        try:
            user_info = self.api.account.verify_credentials()
            # guard against errors bubbling up from the twitter response itself
            try:
                user = None
                try:
                    twitter_token = self.manager.get_uid(user_info['id'])
                    self.update_existing_token(twitter_token, self.token)
                    user = twitter_token.user
                except TwitterToken.DoesNotExist:
                    user = self.manager.create_new_twitter_user(user_info, self.token, self.user_manager)
                return user
            except KeyError:
                return None
        except:
            return None 

    def get_http(self):
        return get_twitter_http()
    
    def get_api(authorized_http):
        return get_twitter_api(authorized_http)

    def get_request_token(self, request):
        request_token = request.session.get(TWITTER_SESSION_KEY, None)
        return request_token

    def authorize_http(self, http, request_token):
        http = self.get_http()
        http.token = request_token
        access_token = http.fetch_access_token()
        http.add_credentials(http.consumer, access_token, 'twitter.com')
        return http

    def setup_api_and_token(self, request):
        request_token = self.get_request_token(request)
        http = self.get_http()
        http = self.authorize_http(http)
        self.api, self.token = self.get_api(http), http.token    

    def update_existing_token(self, twitter_token, token):
        twitter_token.key, twitter_token.secret = token.key, token.secret
        twitter_token.save()
