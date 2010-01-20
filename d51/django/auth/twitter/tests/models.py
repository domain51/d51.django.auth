from d51.django.auth.twitter.models import TwitterToken
from d51.django.auth.twitter.utils import create_new_user
from django.test import TestCase
import oauth2

class TestOfTwitterModels(TestCase):
    def test_get_oauth_token(self):
        twitter_token = TwitterToken.objects.create(user=create_new_user('100', 'chris dickinson'), key='key', secret='secret', uid='100')
        oauth_token = twitter_token.get_oauth_token()
        self.assertTrue(isinstance(oauth_token, oauth2.Token))
        self.assertEqual(oauth_token.key, twitter_token.key)
        self.assertEqual(oauth_token.secret, twitter_token.secret)


