import pkg_resources
pkg_resources.declare_namespace(__name__)

from d51.django.auth.twitter.tests.backends import *
from d51.django.auth.twitter.tests.models import *
from d51.django.auth.twitter.tests.views import *
from d51.django.auth.twitter.tests.utils import *
