d51.django.auth
===============
Extends Django's built-in django.contrib.auth application, providing additional
methods of authentication.


Supported Authentication Methods
--------------------------------
* Email-Only (TODO)
* Facebook Connect
* Twitter OAuth

### Email-Only
*TODO: Carry this over from the old repository*

This extends the basic ModelBackend code to check against the User.email field.
Add the following to your `settings.py` file to switch to the email only
backend exclusively.

    AUTHENTICATION_BACKENDS = (
        'd51.django.auth.emailonly.backends.EmailOnlyBackend',
    )

The email only backend falls back on the basic `ModelBackend` in the event it
can't locate a user by email address.  You can use it as a replacement to
Django's built-in `ModelBackend` and still allow users with usernames to login
using those usernames or their email addresses.


### Facebook Connect
This adds a backend capable of talking with Facebook Connect to handle
authentication.  Add the following to your 'settings.py' file to switch to
Facebook Connect exclusively for your authentication.

    AUTHENTICATION_BACKENDS = (
        'd51.django.auth.facebook.backends.FacebookConnectBackend',
    )

You way want to use an additional authentication mechanism as well.  For
example, use a setting like this if you want to use Facebook Connect in
addition to the email only backend:

    AUTHENTICATION_BACKENDS = (
        'd51.django.auth.emailonly.backends.EmailOnlyBackend',
        'd51.django.auth.facebook.backends.FacebookConnectBackend',
    )

You will also have to add this app to your installed apps, and run migrations.

    INSTALLED_APPS = (
            ... your installed apps ...
            'd51.django.auth.facebook.models',
    )

Afterwards, run `./manage.py syncdb` (or `./manage.py migrate`, if south
is installed). This provides the FacebookID helper model.

### Twitter OAuth
This adds a backend that will talk to Twitter OAuth to handle
authentication. Add the following to your 'settings.py' file to switch to
Twitter OAuth.

    AUTHENTICATION_BACKENDS = (
        'd51.django.auth.twitter.backends.TwitterBackend',
    )

You will also have to add this app to your installed apps, and run migrations.

    INSTALLED_APPS = (
            ... your installed apps ...
            'd51.django.auth.twitter.models',
    )

Afterwards, run `./manage.py syncdb` (or `./manage.py migrate`, if south
is installed). This provides the TwitterToken helper model, which can be used
in conjunction with the `d51.django.auth.twitter.utils` functions to obtain
authenticated API access to Twitter.

Installation
------------
*TODO*

Testing
-------
*TODO: Expand*

Initialize the environment:

    prompt> fab init

Activate the virtualenv:

    prompt> source bin/activate

Then run either of these:

    prompt> fab test
    # or
    prompt> python ./run_tests.py


Usage
-----
*TODO*


