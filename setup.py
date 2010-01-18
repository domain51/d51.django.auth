from distutils.core import setup
import os

# Borrowed and modified from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('d51'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    pkg = dirpath.replace(os.path.sep, '.')
    if os.path.altsep:
        pkg = pkg.replace(os.path.altsep, '.')
    packages.append(pkg)

setup(
    name='d51.django.auths',
    version='0.1', # TODO: move this into Dolt.get_version()
    description='Simple package for running isolated Django tests from within virtualenv',
    author='Domain51',
    author_email='official@domain51.com',
    url='http://github.com/domain51/d51.django.auth/',
    download_url='http://cloud.github.com/downloads/domain51/d51.django.auth/d51.django.auth-0.1.tar.gz',
    packages=packages,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Common Development and Distribution License (CDDL)',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)'
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)


