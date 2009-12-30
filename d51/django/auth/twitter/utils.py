from oauth.oauth import OAuthConsumer, OAuthToken
from oauthclient.twitter import TwitterHttp
from django.conf import settings as django_settings
from dolt.apis.twitter import Twitter as DoltTwitter

TWITTER_SESSION_KEY = 'twitter_request_token'
TWITTER_SESSION_REDIRECT = 'redirect_to'

def get_key_and_secret(settings=django_settings):
    return (
        django_settings.D51_DJANGO_AUTH['TWITTER_CONSUMER_KEY'],
        django_settings.D51_DJANGO_AUTH['TWITTER_CONSUMER_SECRET'],
    )

def get_configured_consumer():
    _consumer_key, _consumer_secret = get_key_and_secret()
    return OAuthConsumer(_consumer_key, _consumer_secret)

def get_twitter_http():
    twitter = TwitterHttp()
    twitter.consumer = get_configured_consumer()
    return twitter

def get_twitter_api(http):
    return DoltTwitter(http)
