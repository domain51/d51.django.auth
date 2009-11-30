d51.django.auth
===============
Extends Django's built-in django.contrib.auth application, providing additional
methods of authentication.

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


