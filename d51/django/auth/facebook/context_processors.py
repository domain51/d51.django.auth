from django.conf import settings

def api_key(request):
    return {'FACEBOOK_API_KEY': getattr(settings, 'FACEBOOK_API_KEY', None),}

def facebook(request):
    return {'facebook': getattr(request, 'facebook', None) }
