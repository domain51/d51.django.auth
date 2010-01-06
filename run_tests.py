from django.conf import settings
from django.core.management import call_command

def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'd51.django.auth',
        ),
        # Django replaces all of this, but it still wants it. *shrugs*
        DATABASE_ENGINE='sqlite3'
    )

    # Fire off the tests
    call_command('test', 'auth')

if __name__ == '__main__':
    main()
