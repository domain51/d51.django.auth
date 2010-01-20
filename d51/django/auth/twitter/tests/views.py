from d51.django.auth.twitter.utils import TWITTER_SESSION_KEY
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

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


