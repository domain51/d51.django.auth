from d51.django.auth.twitter.utils import *
from d51.django.auth.twitter.tests.base import TestCase
from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.http import HttpRequest, QueryDict
import oauth2
import random

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


class TestOfBuildAuthorizationUrl(TestCase):
    def test_returns_authorization_url(self):
        token = self.mox.CreateMock(oauth2.Token)
        token.key = 'some-random-key-%d' % random.randint(1, 1000)

        self.assertEqual(
            'https://twitter.com/oauth/authorize?oauth_token=%s' % token.key,
            build_authorization_url(token)
        )

class TestOfGetRequestToken(TestCase):
    def test_returns_none_if_not_available(self):
        request = self.create_mock_request()
        self.assertEqual(None, get_request_token(request))

    def test_returns_token_if_set(self):
        expected_token = random.randint(1, 1000)
        request = self.create_mock_request()
        request.session[TWITTER_SESSION_KEY] = expected_token

        self.assertEqual(expected_token, get_request_token(request))

