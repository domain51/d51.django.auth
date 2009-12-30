from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import auth
from .utils import get_twitter_http, TWITTER_SESSION_KEY, TWITTER_SESSION_REDIRECT 

def initiate_login(request, redirect_field_name = auth.REDIRECT_FIELD_NAME):
    tweb = get_twitter_http()
    request_token = tweb.fetch_request_token()

    request.session[TWITTER_SESSION_KEY] = request_token
    request.session[TWITTER_SESSION_REDIRECT] = request.REQUEST.get(redirect_field_name, '/')
    
    authorization_url = tweb.authorize_token() 
    return redirect(authorization_url)

def login(request):
    user = auth.authenticate(**{'request':request})
    if user:
        auth.login(request, user)
    return HttpResponseRedirect(request.session[TWITTER_SESSION_REDIRECT])

