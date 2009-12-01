from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'd51.django.auth.facebook.views',
    url(r'^login', 'login', name='facebook_login'),
    url(r'^logout', 'logout', name='facebook_logout'),
    url(r'^xd_receiver.htm$', 'xd_receiver', name='facebook_xd_receiver'),
)

