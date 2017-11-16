import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-lazy-image',
    version='0.0.1',
    packages=[
        'django_lazy_image',
    ],
    install_requires=[
        'sorl-thumbnail',
        'Jinja2',
        'django>=1.11,<1.12',
        'django-jinja>=2.2',
    ],
    include_package_data=True,
    description='An image utility that renders images lazily as well as intrinsically sizes them.',
    long_description=README,
    url='https://github.com/dan-gamble/django-lazy-image/',
    author='Dan Gamble',
    author_email='dan@dangamble.co.uk',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
