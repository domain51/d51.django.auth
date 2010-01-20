from d51.django.auth.twitter.utils import create_new_user
from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.test import TestCase

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


