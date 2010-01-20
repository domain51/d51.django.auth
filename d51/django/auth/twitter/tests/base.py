from django.http import HttpRequest
from django.test import TestCase as DjangoTestCase
import mox

class TestCase(DjangoTestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.VerifyAll()

    def create_mock_request(self):
        request = self.mox.CreateMock(HttpRequest)
        request.session = {}
        request.GET = {}
        return request


