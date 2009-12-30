from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import auth
from .utils import get_twitter_http, TWITTER_SESSION_KEY, TWITTER_SESSION_REDIRECT 

def initiate_login(request, redirect_field_name = auth.REDIRECT_FIELD_NAME):
    if request.method != 'POST':
        r = HttpResponse()
        r.status_code = 405
        return r

    tweb = get_twitter_http()
    request_token = tweb.fetch_request_token()

    request.session[TWITTER_SESSION_KEY] = request_token
    request.session[TWITTER_SESSION_REDIRECT] = request.REQUEST.get(redirect_field_name, '/')
    
    authorization_url = tweb.authorize_token() 
    return redirect(authorization_url)

def login(request):
    """ handle login requests for Twitter

        TODO: There's a ton of shared functionality between this and the
        facebook.login() function.  Seems like these could be refactored into a
        callable object that has a few shared methods such as
        get_authenticate_parameters() and is_valid_login_request() and remove
        the duplication.
    """
    # TODO: check for an existing TwitterToken first

    user = auth.authenticate(request)

    if not user is None:
        auth.login(request, user)

    return HttpResponseRedirect(request.session[TWITTER_SESSION_REDIRECT])

