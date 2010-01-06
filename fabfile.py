from fabric.api import local

def test():
    """
    Run tests for d51.django.apps.schedules
    """
    local("python ./run_tests.py")

def init():
    """
    Initialize a virtualenv in which to run tests against this
    """
    local("virtualenv .")
    local("pip install -E . -r requirements.txt")

def clean():
    """
    Remove the cruft created by virtualenv and pip
    """
    local("rm -rf bin/ include/ lib/")

