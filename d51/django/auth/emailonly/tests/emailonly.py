from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.test import TestCase
from d51.django.auth.emailonly import EmailOnlyBackend

__all__ = [
    'TestOfEmailOnlyAuthentication',
]

def generate_email_only_user():
    travis = User.objects.create(email='travis@example.com')
    travis.set_password('foobar')
    travis.save()
    return travis

def generate_username_only_user():
    chris = User.objects.create(username='chris')
    chris.set_password('foobar')
    chris.save()
    return chris

class TestOfEmailOnlyAuthentication(TestCase):
    def test_is_a_subclass_of_ModelBackend(self):
        auth = EmailOnlyBackend()
        self.assert_(isinstance(auth, ModelBackend))

    def test_returns_none_if_nothing_provided(self):
        auth = EmailOnlyBackend()
        self.assertEqual(None, auth.authenticate())

    def test_returns_none_if_no_password_is_provided(self):
        auth = EmailOnlyBackend()
        self.assertEqual(None, auth.authenticate(username='travis@example.com'))

    def test_returns_user_if_found(self):
        travis = generate_email_only_user()
        auth = EmailOnlyBackend()
        user = auth.authenticate(username = 'travis@example.com', password='foobar')

        self.assert_(isinstance(user, User))
        self.assertEqual(user, travis)

        travis.delete()

    def test_returns_none_if_password_does_not_match(self):
        travis = generate_email_only_user()
        auth = EmailOnlyBackend()
        user = auth.authenticate(username='travis@example.com', password='barfoo')

        self.assertEqual(None, user)
        travis.delete()

    def test_returns_none_if_user_not_found(self):
        auth = EmailOnlyBackend()
        self.assertEqual(None, auth.authenticate(username='unknown@example.com', password='foobar'))

    def test_falls_back_on_real_username_if_email_not_found(self):
        chris = generate_username_only_user()
        auth = EmailOnlyBackend()
        user = auth.authenticate(username='chris', password='foobar')
        self.assertEqual(user, chris)

