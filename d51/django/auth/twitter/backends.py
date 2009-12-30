from d51.django.auth.backends import AbstractModelAuthBackend 
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from .models import TwitterToken
from .utils import TWITTER_SESSION_KEY, get_twitter_http, get_twitter_api, get_configured_consumer, get_key_and_secret

TWITTER_BACKEND_STRING = 'd51.django.auth.facebook.backends.TwitterBackend'

class TwitterBackend(AbstractModelAuthBackend):
    def __init__(self, manager=TwitterToken.objects, settings=django_settings, *args, **kwargs):
        self.manager = manager
        self._consumer_key, self._consumer_secret = get_key_and_secret(django_settings)
        super(TwitterBackend, self).__init__(*args, **kwargs)

    def authenticate(self, **credentials):
        request = credentials.get('request', None)
        if request is None:
            return

        request_token = request.session.get(TWITTER_SESSION_KEY, None)
        if request_token is None:
            return

        tweb = get_twitter_http()
        tweb.token = request_token
        access_token = tweb.fetch_access_token()
        tweb.add_credentials(tweb.consumer, access_token, 'twitter.com')

        api = get_twitter_api(tweb)
        user_info = api.account.verify_credentials()

        user = None
        try:
            ttoken = self.manager.get(uid=user_info['id'])
            ttoken.key = tweb.token.key
            ttoken.secret = tweb.token.secret
            ttoken.save()
            user = ttoken.user
        except TwitterToken.DoesNotExist:
            username = 'tw$%s' % user_info['id']
            name = user_info['name'].split(' ', 1) + [""]
            user, created = self.user_manager.get_or_create(
                                username=username,
                                first_name=name[0],
                                last_name=name[1],
            )
            user.set_unusable_password()
            user.save()
            self.manager.create(
                uid=user_info['id'],
                user=user,
                key=tweb.token.key,
                secret=tweb.token.secret,
            )
        return user
