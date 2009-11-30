import pkg_resources
pkg_resources.declare_namespace(__name__)

from django.contrib.auth.models import User

class EmailOnlyBackend():
    def authenticate(self, username=None, password=None):
        if not username or not password:
            return None

        user = User.objects.get(email=username)
        if user.check_password(password):
            return user

