d51.django.auth
===============
Extends Django's built-in django.contrib.auth application, providing additional
methods of authentication.


Supported Authentication Methods
--------------------------------
* Email-Only (TODO)
* Facebook Connect
* Twitter OAuth (not-yet implemented)

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


### Twitter OAuth
*TODO*


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


