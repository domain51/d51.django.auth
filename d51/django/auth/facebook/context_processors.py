from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY
from .backends import FACEBOOK_CONNECT_BACKEND_STRING 

def api_key(request):
    return {'FACEBOOK_API_KEY': getattr(settings, 'FACEBOOK_API_KEY', None),}

def facebook(request):
    facebook = getattr(request, 'facebook', None)
    is_logged_in = request.session.get(BACKEND_SESSION_KEY, None) == FACEBOOK_CONNECT_BACKEND_STRING
    return {
        'facebook': getattr(request, 'facebook', None),
        'facebook_is_logged_in': is_logged_in,
    }
