from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.conf import settings
from django.core.urlresolvers import reverse
from d51.django.auth.twitter.backends import TwitterBackend
from dolt import Dolt
from random import randint as random
from .utils import TWITTER_SESSION_KEY, TWITTER_SESSION_REDIRECT, TwitterHttp, create_new_user
from .models import TwitterToken
import oauth2

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

class TestOfTwitterModels(TestCase):
    def test_get_oauth_token(self):
        twitter_token = TwitterToken.objects.create(user=create_new_user('100', 'chris dickinson'), key='key', secret='secret', uid='100')
        oauth_token = twitter_token.get_oauth_token()
        self.assertTrue(isinstance(oauth_token, oauth2.Token))
        self.assertEqual(oauth_token.key, twitter_token.key)
        self.assertEqual(oauth_token.secret, twitter_token.secret)

class TestOfTwitterUtils(TestCase):
    def test_create_new_user(self):
        twitter_info = {
            'name':'chris dickinson',
            'twitter_id':'1010101',
        }
        user = create_new_user(user_manager=User.objects, **twitter_info)
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.password, UNUSABLE_PASSWORD)
        self.assertEqual(user.first_name, 'chris')
        self.assertEqual(user.last_name, 'dickinson')
        self.assertTrue(user.username.startswith('tw$'))

class TestOfTwitterBackend(TestCase):
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

        good_request = bad_request; good_request.session[TWITTER_SESSION_KEY] = oauth2.Token('key', 'secret')
        fake_backend.setup_api_and_token(good_request)
        dolt = fake_backend.api
 
        self.assertTrue(isinstance(dolt, Dolt))

    def test_get_api(self):
        triggers = { 'add_credentials': False }
        class MockHttp(object):
            consumer = None
            token = None
        http = MockHttp()
        backend = TwitterBackend()
        self.assertTrue(isinstance(backend.get_api(), Dolt))

    def test_get_existing_twitter_user(self):
        user = create_new_user('101', 'chris dickinson')
        twitter_token = TwitterToken.objects.create_new_twitter_token(user, '101', oauth2.Token('key', 'secret'))
        class MockDolt(object):
            def __getattr__(self, what):
                return self

            def __call__(self):
                return {
                    'id':'101',
                    'name':'chris dickinson',
                }
        class MockBackend(TwitterBackend):
            api = MockDolt()
            token = oauth2.Token('new-key', 'new-secret')

        backend = MockBackend()
        user_from_backend = backend.get_twitter_user()
        self.assertEqual(user_from_backend.id, user.id)
        self.assertEqual(user_from_backend.twitter.key, 'new-key')
        self.assertEqual(user_from_backend.twitter.secret, 'new-secret')

    def test_get_new_twitter_user(self):
        class MockDolt(object):
            def __getattr__(self, what):
                return self
            def __call__(self):
                return {
                    'id':'102',
                    'name':'chris',
                }
        class MockBackend(TwitterBackend):
            api = MockDolt()
            token = oauth2.Token('key', 'secret')

        backend = MockBackend()
        user = backend.get_twitter_user()
        self.assertEqual(user.first_name, 'chris')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.username, 'tw$102')
        self.assertEqual(user.password, UNUSABLE_PASSWORD)
        self.assertEqual(user.twitter.key, 'key')
        self.assertEqual(user.twitter.secret, 'secret')


    def test_authenticate(self):
        mock_request = object()
        class MockBackend(TwitterBackend):
            def setup_api_and_token(_self, request):
                self.assertEqual(request, mock_request)

            def get_twitter_user(self):
                user = create_new_user('200', 'chris dickinson')
                twitter_token = TwitterToken.objects.create_new_twitter_token(user, '200', oauth2.Token('key', 'secret'))
                return twitter_token.user

        class MockBackendThrows(MockBackend):
            def get_twitter_user(self):
                raise TwitterToken.DoesNotExist()

        backend = MockBackend()
        self.assertEqual(backend.authenticate(non_request=1), None)
        user = backend.authenticate(request=mock_request)
        self.assertTrue(isinstance(user, User)) 
        self.assertEqual(user.twitter.key, 'key')
        self.assertEqual(user.twitter.secret, 'secret')

        backend = MockBackendThrows()
        self.assertRaises(TwitterToken.DoesNotExist, backend.authenticate, request=mock_request)
