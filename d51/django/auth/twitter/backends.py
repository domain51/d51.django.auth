from d51.django.auth.backends import AbstractModelAuthBackend 
from d51.django.auth.twitter import utils
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from .models import TwitterToken

TWITTER_BACKEND_STRING = 'd51.django.auth.facebook.backends.TwitterBackend'

class TwitterBackend(AbstractModelAuthBackend):
    def __init__(self, manager=TwitterToken.objects, utils=utils, settings=django_settings, *args, **kwargs):
        self.manager = manager
        self.utils = utils
        super(TwitterBackend, self).__init__(*args, **kwargs)

    def authenticate(self, **credentials):
        request = credentials.get('request', None)
        if request is None:
            return

        request_token = self.utils.get_request_token(request)

        access_token = self.utils.fetch_access_token(request_token, request.GET.get('oauth_token'))

        twitter = self.utils.get_twitter_api(token=access_token)
        user_info = twitter.account.verify_credentials()
        try:
            twitter_token = self.manager.get_uid(user_info['id'])
            twitter_token.update_from_oauth_token(access_token)
        except TwitterToken.DoesNotExist:
            user = self.utils.create_new_user(user_info['id'], user_info['name'], user_manager=self.user_manager)
            twitter_token = self.manager.create_new_twitter_token(user, user_info['id'], access_token)
 
        return twitter_token.user

