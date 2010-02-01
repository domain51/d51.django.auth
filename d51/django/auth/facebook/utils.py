from facebook.djangofb import Facebook
from django.conf import settings as django_settings

def get_facebook_settings(settings=django_settings):
    setting_keys_and_defaults = {
        'api_key':('FACEBOOK_API_KEY',None),
        'secret_key':('FACEBOOK_SECRET_KEY',None),
        'app_name':('FACEBOOK_APP_NAME',None),
        'callback_path':('FACEBOOK_CALLBACK_PATH',None),
        'internal':('FACEBOOK_INTERNAL',True),
        'proxy':('USE_HTTP_PROXY', getattr(settings, 'HTTP_PROXY', None)),
    }
    return dict([
        (key, getattr(settings, *args))
        for key, args in setting_keys_and_defaults.iteritems()
    ])

def get_facebook_api(for_uid=None):
    facebook_api = Facebook(**get_facebook_settings())
    if for_uid:
        facebook_api.uid = for_uid
    return facebook_api
