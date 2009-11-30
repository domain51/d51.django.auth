from django.contrib.auth.models import User
from django.test import TestCase
from d51.django.auth.emailonly import EmailOnlyBackend

__all__ = [
    'TestOfEmailOnlyAuthentication',
]

def generate_travis():
    travis = User.objects.create(email='travis@example.com')
    travis.set_password('foobar')
    travis.save()
    return travis

class TestOfEmailOnlyAuthentication(TestCase):
    def test_returns_none_if_nothing_provided(self):
        auth = EmailOnlyBackend()
        self.assertEqual(None, auth.authenticate())

    def test_returns_none_if_no_password_is_provided(self):
        auth = EmailOnlyBackend()
        self.assertEqual(None, auth.authenticate(username='travis@example.com'))

    def test_returns_user_if_found(self):
        travis = generate_travis()
        auth = EmailOnlyBackend()
        user = auth.authenticate(username = 'travis@example.com', password='foobar')

        self.assert_(isinstance(user, User))
        self.assertEqual(user, travis)

        travis.delete()

    def test_returns_none_if_password_does_not_match(self):
        travis = generate_travis()
        auth = EmailOnlyBackend()
        user = auth.authenticate(username='travis@example.com', password='barfoo')

        self.assertEqual(None, user)
