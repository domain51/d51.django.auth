from django.contrib.auth import BACKEND_SESSION_KEY
from .backends import TWITTER_BACKEND_STRING
def twitter(request):
    is_logged_in = request.session.get(BACKEND_SESSION_KEY, None) == TWITTER_BACKEND_STRING
    return {
        'twitter_is_logged_in':is_logged_in,
    }
