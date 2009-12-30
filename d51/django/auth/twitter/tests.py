from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from d51.django.auth.twitter.backends import TwitterBackend
from random import randint as random

class TestOfTwitterViews(TestCase):
    def setUp(self):
        self.initial_login_url = reverse('d51.django.auth.twitter.views.initiate_login')

    def test_generates_405_on_non_post(self):
        c = Client()
        response = c.get(self.initial_login_url)
        self.assertEqual(405, response.status_code)

    def test_redirects_to_twitter_for_authentication(self):
        c = Client()
        res = c.post(self.initial_login_url)
        self.assertNotEqual("", c.session['twitter_request_token'])

        redirect_url = res._headers['location'][1]
        expected_url = "http://twitter.com/oauth/authorize"
        self.assertEqual(
            redirect_url[0:len(expected_url)],
            expected_url,
            "should redirect to %s" % expected_url
        )

class TestOfTwitterBackend_get_twitter(TestCase):
    def test_uses_configured_settings(self):
        auth = TwitterBackend()
        consumer = auth._get_twitter()._Consumer
        self.assertEquals(settings.D51_DJANGO_AUTH['TWITTER']['CONSUMER_KEY'], consumer.key)
        self.assertEquals(settings.D51_DJANGO_AUTH['TWITTER']['CONSUMER_SECRET'], consumer.secret)

