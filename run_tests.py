from django.conf import settings
from django.conf.urls.defaults import patterns, include, handler500
from django.core.management import call_command
import ConfigParser, os, sys

handler500
urlpatterns = patterns('',
    (r'^twitter/', include('d51.django.auth.twitter.urls')),
)

def main():
    # Check to see that ~/.d51.django.auth.test.settings file is available
    settings_file = os.path.join(os.environ['HOME'], '.d51.django.auth.test.settings')
    if not os.path.exists(settings_file):
        print """
Please create a ~/.d51.django.auth.test.settings config file with the following
in it (be sure to fill in your settings).  You must register your own Twitter
oauth client to run these tests:

[settings]
TWITTER_CONSUMER_KEY = <your consumer key>
TWITTER_CONSUMER_SECRET = <your consumer secret>

""".lstrip()
        sys.exit(1)

    config = ConfigParser.RawConfigParser()
    config.read(settings_file)

    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'd51.django.auth',
            'd51.django.auth.facebook',
            'd51.django.auth.twitter',
        ),
        # Django replaces all of this, but it still wants it. *shrugs*
        DATABASE_ENGINE='sqlite3',

        # Make this the urls.py and include the necessary patterns here
        ROOT_URLCONF='run_tests',

        # Necessary configuration for d51.django.auth
        D51_DJANGO_AUTH = {
            'TWITTER_CONSUMER_KEY': config.get('settings', 'TWITTER_CONSUMER_KEY'),
            'TWITTER_CONSUMER_SECRET': config.get('settings', 'TWITTER_CONSUMER_SECRET'),
        },

    )

    # Fire off the tests
    call_command('test', 'auth')

if __name__ == '__main__':
    main()
