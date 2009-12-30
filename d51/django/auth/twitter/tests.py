from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.conf import settings
from django.core.urlresolvers import reverse
from d51.django.auth.twitter.backends import TwitterBackend
from dolt import Dolt
from random import randint as random
from .utils import TWITTER_SESSION_KEY, TWITTER_SESSION_REDIRECT, TwitterHttp
from .models import TwitterToken
from oauth.oauth import OAuthToken

class TestOfTwitterViews(TestCase):
    def setUp(self):
        self.initial_login_url = reverse('d51.django.auth.twitter.views.initiate_login')

    def test_redirects_to_twitter_for_authentication(self):
        c = Client()
        res = c.post(self.initial_login_url)
        self.assertNotEqual("", c.session[TWITTER_SESSION_KEY])

        redirect_url = res._headers['location'][1]
        expected_url = "http://twitter.com/oauth/authorize"
        self.assertEqual(
            redirect_url[0:len(expected_url)],
            expected_url,
            "should redirect to %s" % expected_url
        )

class TestOfTwitterBackend(TestCase):
    def test_get_existing_user(self):
        user = User.objects.create(username='exists')
        ttoken = TwitterToken.objects.create(user=user, key='', secret='', uid=1)
        backend = TwitterBackend()
        token = OAuthToken('key', 'secret')
        backend_user = backend.get_existing_user({'id':1},token)
        self.assertEqual(backend_user, user)
        self.assertEqual(backend_user.twittertoken.key, token.key)
        self.assertEqual(backend_user.twittertoken.secret, token.secret)
        self.assertRaises(TwitterToken.DoesNotExist, backend.get_existing_user, {'id':2}, token)
        user.delete()

    def test_create_new_user(self):
        twitter_info = {
            'name':'chris dickinson',
            'id':'1010101',
        }
        token = OAuthToken('key', 'secret')
        backend = TwitterBackend()

        user = backend.create_new_user(twitter_info, token)
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.twittertoken.key, token.key)
        self.assertEqual(user.twittertoken.secret, token.secret)
        self.assertEqual(user.password, UNUSABLE_PASSWORD)
        self.assertEqual(user.first_name, 'chris')
        self.assertEqual(user.last_name, 'dickinson')
        self.assertTrue(user.username.startswith('tw$'))

    def test_setup_api_and_token(self):
        class FakeRequest(object):
            session = { 
                TWITTER_SESSION_KEY:None,
            }
        bad_request = FakeRequest()
        triggers = {'fetch_access_token':False, 'add_credentials':False}

        class FakeTwitterHttp(TwitterHttp):
            token = None
            consumer = None
            def fetch_access_token(self):
                triggers['fetch_access_token'] = True
                return self.token
            def add_credentials(self, consumer, token, domain):
                triggers['add_credentials'] = True

        class FakeBackend(TwitterBackend):
            def get_http(self):
                return FakeTwitterHttp()

        fake_backend = FakeBackend()
        self.assertEqual(fake_backend.setup_api_and_token(bad_request), None)

        good_request = bad_request; good_request.session[TWITTER_SESSION_KEY] = OAuthToken('key', 'secret')
        dolt, token = fake_backend.setup_api_and_token(good_request)

        self.assertTrue(isinstance(dolt, Dolt))
        self.assertTrue(isinstance(token, OAuthToken))
        self.assertTrue(triggers['fetch_access_token'])
        self.assertTrue(triggers['add_credentials'])

    def test_authenticate(self):
        class FakeApi(object):
            def __getattr__(self, name):
                return self
            def __call__(self):
                return self

        gary_busey = User.objects.create(username='Gary Busey')
        lary_goosy = User.objects.create(username='Lary Goosy')
        class FakeBackend(TwitterBackend):
            def __init__(self, find_token, *args, **kwargs):
                self.find_token = find_token
                return super(FakeBackend, self).__init__(*args,**kwargs)
            def setup_api_and_token(self, *args, **kwargs):
                return FakeApi(), OAuthToken('key', 'secret')
            def get_existing_user(self, *args, **kwargs):
                if self.find_token:
                    return gary_busey
                else:
                    raise TwitterToken.DoesNotExist()
            def create_new_user(self, *args, **kwargs):
                return lary_goosy

        backend = FakeBackend(True)
        results = backend.authenticate(**{'request':object()})
        self.assertEqual(results, gary_busey)

        backend = FakeBackend(False)
        results = backend.authenticate(**{'request':object()})
        self.assertEqual(results, lary_goosy)

