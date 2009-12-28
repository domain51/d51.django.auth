from django.shortcuts import redirect

# Yes, the ".." is necessary and not some weird typo.  It's required because
# Python doesn't continue looking through the path when it has a possible
# match.  Doing "from facebook import" here causes Python to stop as soon as
# it gets to d51.django.auth.facebook.
from .. facebook import FacebookError
from facebook.models import FacebookID

def _do_logout_redirect(redirect_to):
    response = redirect('d51.django.auth.facebook.views.logout')
    response['Location'] += '?next=%s' % redirect_to
    return response

def is_fully_authenticated(request):
    if not request.user.is_active or not request.user.is_authenticated():
        return False
    elif is_facebook_user(request.user):
        try:
            if not request.facebook.check_session(request):
                return False
            try:
                request.facebook.users.getLoggedInUser()
                return True
            except FacebookError, e:
                if e.code == 102:
                    return False
                else:
                    raise
        except Exception:
            # handle any weird exception from Facebook
            return True
    return True

# TODO: move this into the d51.django.auth.facebook portion of the code
def is_facebook_user(user):
    try:
        return getattr(user, 'facebook', False)
    except FacebookID.DoesNotExist:
        return False

def auth_required(redirect_to = '/'):
    def decorator(view):
        def newview(request, *args, **kwargs):
            if not is_fully_authenticated(request):
                return _do_logout_redirect(redirect_to)
            return view(request, *args, **kwargs)
        return newview
    return decorator

