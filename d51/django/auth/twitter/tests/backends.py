from django.conf import settings
from django.contrib.auth.models import User, UserManager, UNUSABLE_PASSWORD
from d51.django.auth.twitter.backends import TwitterBackend
from dolt import Dolt
import random
from d51.django.auth.twitter import managers, models, utils
from d51.django.auth.twitter.utils import TWITTER_SESSION_KEY, TWITTER_SESSION_REDIRECT, TwitterHttp, create_new_user
from d51.django.auth.twitter.models import TwitterToken
from d51.django.auth.twitter.tests.base import TestCase
import oauth2

# These classes are for Mox
class MockTwitterAccount(object):
    def verify_credentials(self):
        pass

class MockTwitter(object):
    account = MockTwitterAccount()


class TestOfTwitterBackend(TestCase):
    def setUp_authenticate_returns_new_user_if_none_found(self):
        # TODO: refactor so this doesn't make my eyes bleed
        random_user_id = random.randint(1, 1000)
        random_user_name = 'Bob Smith (%d)' % random_user_id
        mock_twitter = self.mox.CreateMock(MockTwitter)
        mock_twitter.account = self.mox.CreateMock(MockTwitterAccount)
        mock_twitter.account.verify_credentials().AndReturn({
            'id': random_user_id,
            'name': random_user_name,
        })

        user = self.mox.CreateMock(User)
        manager = self.mox.CreateMock(managers.TwitterTokenManager)
        manager.get_uid(random_user_id).AndRaise(TwitterToken.DoesNotExist)

        user_manager = self.mox.CreateMock(UserManager)

        request = self.create_mock_request()
        random_oauth_token = random.randint(1, 1000)
        request.GET['oauth_token'] = random_oauth_token
        self.mox.StubOutWithMock(utils, 'create_new_user')
        self.mox.StubOutWithMock(utils, 'get_twitter_api')
        self.mox.StubOutWithMock(utils, 'get_request_token')
        self.mox.StubOutWithMock(utils, 'fetch_access_token')
        utils.get_request_token(request).AndReturn('123')
        utils.get_twitter_api(token='123').AndReturn(mock_twitter)
        utils.create_new_user(random_user_id, random_user_name, user_manager=user_manager).AndReturn(user)
        random_token_key = 'some key %d' % random.randint(1, 1000)
        random_token_secret = 'some secret %d' % random.randint(1, 1000)
        token = oauth2.Token(random_token_key, random_token_secret)
        manager.create_new_twitter_token(user, random_user_id, token)
        utils.fetch_access_token('123', random_oauth_token).AndReturn(token)
        self.mox.ReplayAll()
        return (request, manager, user_manager)

    def test_authenticate_returns_new_user_if_none_found(self):
        request, manager, user_manager = self.setUp_authenticate_returns_new_user_if_none_found()
        backend = TwitterBackend(manager=manager, user_manager=user_manager)
        backend.authenticate(request=request)


    def test_returns_existing_user_with_updated_token(self):
        # TODO: create test
        pass

