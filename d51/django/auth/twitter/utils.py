from oauth.oauth import OAuthConsumer, OAuthToken
from oauthclient.twitter import TwitterHttp
from django.conf import settings as django_settings
from dolt.apis.twitter import Twitter as DoltTwitter
from django.contrib.auth.models import User, UNUSABLE_PASSWORD

TWITTER_SESSION_KEY = 'twitter_request_token'
TWITTER_SESSION_REDIRECT = 'redirect_to'

def get_key_and_secret(settings=django_settings):
    return (
        settings.D51_DJANGO_AUTH['TWITTER_CONSUMER_KEY'],
        settings.D51_DJANGO_AUTH['TWITTER_CONSUMER_SECRET'],
    )

def get_configured_consumer():
    _consumer_key, _consumer_secret = get_key_and_secret()
    return OAuthConsumer(_consumer_key, _consumer_secret)

def get_twitter_http():
    twitter = TwitterHttp()
    twitter.consumer = get_configured_consumer()
    return twitter

def get_twitter_api(http):
    http.add_credentials(http.consumer, http.token, 'twitter.com')
    return DoltTwitter(http)

def create_new_user(twitter_id, name, user_manager=User.objects):
    username = 'tw$%s'%twitter_id
    name = name.split(' ',1)+['']           # ensure that the length of the resultant array is always at least 2
    return user_manager.create(
                username=username,
                first_name=name[0],
                last_name=name[1],
                password=UNUSABLE_PASSWORD
    )
