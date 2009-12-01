from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib import auth
from django.contrib.auth.views import logout as django_logout
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, HttpResponse

def login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    """ Handles logging in a user from Facebook Connect

        @todo redirect on invalid login
        @todo This and twitter.login() are going to be almost identical,
              refactor to remove duplication.
    """
    if not hasattr(request, 'facebook'):
        raise ImproperlyConfigured(
            'd51_django_auth.views.login requires that the PyFacebook '
            'middleware (facebook.djangofb.FacebookMiddleware) be enabled in '
            'order to login.  Please add it to your site\'s MIDDLEWARE_CLASSES'
        )

    user = auth.authenticate(request = request)
    if not user is None:
        auth.login(request, user)

    redirect_to = request.REQUEST.get(redirect_field_name, '/')
    return HttpResponseRedirect(redirect_to)

def xd_receiver(request):
    return HttpResponse(
"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<body>
    <script src="http://static.ak.connect.facebook.com/js/api_lib/v0.4/XdCommReceiver.js" type="text/javascript"></script>
</body>
</html>""")

def logout(request, *args, **kwargs):
    """ Handles logging a user out of system after logging out of FB Connect

        This passes off to django.contrib.auth.views.logout to handle the
        Django specific pieces after it deletes the appropriate cookies
        for Facebook Connect.
    """
    response = django_logout(request, *args, **kwargs)

    api_key_len = len(settings.FACEBOOK_API_KEY)
    for (cookie_name, cookie_value) in request.COOKIES.iteritems():
        if cookie_name[0:api_key_len] != settings.FACEBOOK_API_KEY:
            continue
        response.delete_cookie(cookie_name)
    return response

