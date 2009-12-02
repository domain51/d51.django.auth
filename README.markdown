d51.django.auth
===============
Extends Django's built-in django.contrib.auth application, providing additional
methods of authentication.


Supported Authentication Methods
--------------------------------
* Email-Only
* Facebook Connect
* Twitter OAuth (not-yet implemented)

### Email-Only
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
d51.django.auth uses Buildout to manage its internal dependencies for testing
purposes.  Using this repository directly via a Git clone causes issues that
since Buildout creates a new `project/` directory inside it's project.  Using
Fabric, this is neutralized by putting the directory in a temporary location.

You can run Buildout directly to prepare the repository for testing, or you can
run it using Fabric:

    prompt> fab init

You need to run that only once.

Now you can test using Fabric as well:

    prompt> fab test

Rename the `project-for-testing` directory to `project` to run the tests using
Django's built-in test runner.  Once it is renamed, you can run the following
to run tests:

    prompt> bin/django test auth_tests

Or, you can run the tests for individual backends.  For example, to run the
tests for the email only backend:

    prompt> bin/django test emailonly


Usage
-----
*TODO*


