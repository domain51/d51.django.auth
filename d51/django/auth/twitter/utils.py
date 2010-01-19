import cgi
from django.conf import settings as django_settings
from dolt.apis.twitter import Twitter as TwitterHttp
from django.contrib.auth.models import User, UNUSABLE_PASSWORD
import oauth2

TWITTER_SESSION_KEY = 'twitter_request_token'
TWITTER_SESSION_REDIRECT = 'redirect_to'

def fetch_request_token():
    http = get_http_client()
    request_token_url = 'https://twitter.com/oauth/request_token'
    (response, body) = http.request(request_token_url, 'GET')
    request_token = oauth2.Token.from_string(body)
    return request_token

def fetch_access_token(request_token, oauth_token):
    access_token_url = "http://twitter.com/oauth/access_token"
    http = get_http_client(token=request_token)
    (resp, body) = http.request(access_token_url, 'POST', 'oauth_token=%s' % oauth_token)
    return oauth2.Token.from_string(body)


def get_key_and_secret(settings=django_settings):
    return (
        settings.D51_DJANGO_AUTH['TWITTER_CONSUMER_KEY'],
        settings.D51_DJANGO_AUTH['TWITTER_CONSUMER_SECRET'],
    )

def get_configured_consumer():
    return oauth2.Consumer(*get_key_and_secret())

def get_http_client(consumer=None, token=None):
    consumer = consumer and consumer or get_configured_consumer()
    return oauth2.Client(consumer, token)
    
def get_twitter_api(consumer=None, token=None):
    return TwitterHttp(get_http_client(consumer=consumer, token=token))

def create_new_user(twitter_id, name, user_manager=User.objects):
    username = 'tw$%s'%twitter_id
    name = name.split(' ',1)+['']           # ensure that the length of the resultant array is always at least 2
    return user_manager.create(
                username=username,
                first_name=name[0],
                last_name=name[1],
                password=UNUSABLE_PASSWORD
    )
