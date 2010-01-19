import cgi
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import auth
from d51.django.auth.twitter import utils
from .utils import TWITTER_SESSION_KEY, TWITTER_SESSION_REDIRECT, get_twitter_api
import oauth2

def initiate_login(request, redirect_field_name = auth.REDIRECT_FIELD_NAME):
    request_token = utils.fetch_request_token()
    request.session[TWITTER_SESSION_KEY] = request_token
    request.session[TWITTER_SESSION_REDIRECT] = request.REQUEST.get(redirect_field_name, '/')
  
    # TODO: should this be encoded?
    # TODO: Should this be redirected to https?
    authorization_url = 'http://twitter.com/oauth/authorize?oauth_token=%s' % request_token.key
    return redirect(authorization_url)

def login(request):
    user = auth.authenticate(request=request)
    if user:
        auth.login(request, user)
    return HttpResponseRedirect(request.session[TWITTER_SESSION_REDIRECT])

