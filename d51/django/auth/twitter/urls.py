from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'd51.django.auth.twitter.views',
    url(r'^initiate_login/?$', 'initiate_login', name = 'twitter_initiate_login'),
    url(r'^login/?$', 'login', name = 'twitter_login'),
)

