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

        api, token = self.setup_api_and_token(request) 

        if api is None:
            return

        # guard against anything bubbling up through Dolt
        try:
            user_info = api.account.verify_credentials()
            # guard against errors bubbling up from the twitter response itself
            try:
                user = None
                try:
                    user = self.get_existing_user(user_info, token)
                except TwitterToken.DoesNotExist:
                    user = self.create_new_user(user_info, token)
                return user
            except KeyError:
                return None
        except:
            return None 
    def get_existing_user(self, twitter_info, token):
        ttoken = self.manager.get(uid=twitter_info['id'])
        ttoken.key, ttoken.secret = token.key, token.secret
        ttoken.save()
        return ttoken.user

    def create_new_user(self, twitter_info, token):
        username = 'tw$%s' % twitter_info['id']
        name = twitter_info['name'].split(' ', 1) + [""]
        user, created = self.user_manager.get_or_create(
                            username=username,
                            first_name=name[0],
                            last_name=name[1],
        )
        user.set_unusable_password()
        user.save()
        self.manager.create(
            uid=twitter_info['id'],
            user=user,
            key=token.key,
            secret=token.secret,
        )
        return user

    def get_http(self):
        return get_twitter_http()

    def setup_api_and_token(self, request):
        request_token = request.session.get(TWITTER_SESSION_KEY, None)
        if request_token is None:
            return None

        tweb = self.get_http()
        tweb.token = request_token
        access_token = tweb.fetch_access_token()
        tweb.add_credentials(tweb.consumer, access_token, 'twitter.com')
        return get_twitter_api(tweb), tweb.token 
