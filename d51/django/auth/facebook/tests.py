from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.http import HttpRequest
from d51.django.auth.facebook.backends import FacebookConnectBackend, FACEBOOK_CONNECT_BACKEND_STRING
from d51.django.auth.facebook.managers import FacebookIDManager
from d51.django.auth.facebook.models import FacebookID
from facebook import Facebook
import mox
from random import randint as random

# Required to mock this out since its generated dynamically and Mox
# can't/won't create stuff just for the hell of it.
class StubUserProxy(object):
    def getInfo(self, list):
        pass

def replay_all(*args):
    [mox.Replay(obj) for obj in args]

def verify_all(*args):
    [mox.Verify(obj) for obj in args]

class TestOfFacebookID(TestCase):
    def test_has_custom_manager(self):
        self.assert_(isinstance(FacebookID.objects, FacebookIDManager))

    def test_has_get_uid_method(self):
        random_id = random(10, 1000)
        user = User.objects.create(username="foobar")
        obj = FacebookID.objects.create(pk=random_id, user=user)

        self.assertEqual(obj, FacebookID.objects.get_uid(random_id))

        obj.delete()
        user.delete()


class TestOfFacebookConnectBackend(TestCase):
    def test_returns_none_if_request_not_passed_in(self):
        auth = FacebookConnectBackend()
        self.assertEqual(None, auth.authenticate())

    def test_returns_none_if_check_session_fails(self):
        req = mox.MockObject(HttpRequest)
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(False)
        req.facebook = facebook

        replay_all(facebook, req)

        auth = FacebookConnectBackend()
        self.assertEqual(None, auth.authenticate(request = req))

        verify_all(facebook, req)

    def test_manager_defaults_to_main_FacebookIDManager_if_not_specified(self):
        auth = FacebookConnectBackend()
        self.assertTrue(isinstance(auth.manager, FacebookIDManager))

    def test_uses_custom_manager_if_provided(self):
        obj = object()
        auth = FacebookConnectBackend(manager = obj)
        self.assertEquals(obj, auth.manager)

    def test_user_manager_defaults_to_main_UserManager_if_not_specified(self):
        auth = FacebookConnectBackend()
        self.assertTrue(isinstance(auth.user_manager, UserManager))

    def test_uses_custom_user_manager_if_provided(self):
        obj = object()
        auth = FacebookConnectBackend(user_manager = obj)
        self.assertEquals(obj, auth.user_manager)

    def test_returns_user_if_found(self):
        random_id = random(10, 100)

        user = mox.MockObject(User)
        fb_id = mox.MockObject(FacebookID)
        fb_id.user = user
        fb_manager = mox.MockObject(FacebookIDManager)
        fb_manager.get_uid(random_id).AndReturn(fb_id)

        req = mox.MockObject(HttpRequest)
        req.user = user
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(True)
        facebook.uid = random_id
        req.facebook = facebook

        replay_all(req, facebook, user, fb_id, fb_manager)

        auth = FacebookConnectBackend(manager=fb_manager)
        self.assertEqual(user, auth.authenticate(request=req))

        verify_all(req, facebook, user, fb_id, fb_manager)

    def test_returned_user_has_backend_set_to_facebook_backend(self):
        random_id = random(10, 100)

        user = mox.MockObject(User)
        fb_id = mox.MockObject(FacebookID)
        fb_id.user = user
        fb_manager = mox.MockObject(FacebookIDManager)
        fb_manager.get_uid(random_id).AndReturn(fb_id)

        req = mox.MockObject(HttpRequest)
        req.user = user
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(True)
        facebook.uid = random_id
        req.facebook = facebook

        replay_all(req, facebook, user, fb_id, fb_manager)

        auth = FacebookConnectBackend(manager=fb_manager)
        auth.authenticate(request=req)
        self.assertEqual(FACEBOOK_CONNECT_BACKEND_STRING, req.user.backend)

        verify_all(req, facebook, user, fb_id, fb_manager)



    def test_returns_newly_created_user_if_not_found(self):
        random_id = random(10, 100)
        username = 'fb$%d' % random_id

        user = mox.MockObject(User)
        user.is_authenticated().AndReturn(False)
        user.username = username
        user.set_unusable_password()
        user.save()

        user_manager = mox.MockObject(UserManager)
        user_manager.create(
            username=username,
            first_name='Bob',
            last_name='Example'
        ).AndReturn(user)

        fb_id = mox.MockObject(FacebookID)
        fb_id.user = user

        fb_manager = mox.MockObject(FacebookIDManager)
        fb_manager.model = FacebookID
        fb_manager.get_uid(random_id).AndRaise(FacebookID.DoesNotExist())
        fb_manager.create(pk = random_id, user = user).AndReturn(fb_id)

        req = mox.MockObject(HttpRequest)
        req.user = user
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(True)
        facebook.uid = random_id
        facebook.users = mox.MockObject(StubUserProxy)
        facebook.users.getInfo([random_id], ['name']).AndReturn([{"name": "Bob Example"}])
        req.facebook = facebook

        replay_all(user, user_manager, req, facebook, facebook.users, fb_id, fb_manager)

        auth = FacebookConnectBackend(manager=fb_manager, user_manager=user_manager)
        new_user = auth.authenticate(request = req)
        self.assertTrue(isinstance(new_user, User))

        verify_all(user, user_manager, req, facebook, facebook.users, fb_id, fb_manager)

    def test_creates_new_fb_id_for_existing_user(self):
        random_id = random(10, 100)
        username = 'fb$%d' % random_id

        user = mox.MockObject(User)
        user.is_authenticated().AndReturn(True)

        fb_id = mox.MockObject(FacebookID)
        fb_id.user = user

        req = mox.MockObject(HttpRequest)
        req.user = user
        facebook = mox.MockObject(Facebook)
        facebook.check_session(req).AndReturn(True)
        facebook.uid = random_id
        req.facebook = facebook

        fb_manager = mox.MockObject(FacebookIDManager)
        fb_manager.get_uid(random_id).AndRaise(FacebookID.DoesNotExist())
        fb_manager.model = FacebookID
        fb_manager.create(pk=random_id, user=user).AndReturn(fb_id)

        replay_all(user, req, facebook, fb_manager)

        auth = FacebookConnectBackend(manager=fb_manager)
        new_user = auth.authenticate(request=req)
        self.assertEqual(new_user, user)

        verify_all(user, req, facebook, fb_manager)

    def test_provides_expected_get_user_functionality(self):
        user_id = random(10, 100)
        user = mox.MockObject(User)
        user_manager = mox.MockObject(UserManager)
        user_manager.get(pk = user_id).AndReturn(user)
        replay_all(user, user_manager)

        auth = FacebookConnectBackend(user_manager=user_manager)
        self.assertEqual(user, auth.get_user(user_id))
        verify_all(user, user_manager)

    def test_returns_none_if_no_user_is_found(self):
        user_id = random(10, 100)
        user_manager = mox.MockObject(UserManager)
        user_manager.model = User
        user_manager.get(pk=user_id).AndRaise(User.DoesNotExist)
        replay_all(user_manager)

        auth = FacebookConnectBackend(user_manager=user_manager)
        self.assertEqual(None, auth.get_user(user_id))
        verify_all(user_manager)

