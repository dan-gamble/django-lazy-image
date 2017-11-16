import os
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install

VERSION = '0.0.6'

def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-lazy-image',
    version=VERSION,
    description='An image utility that renders images lazily as well as intrinsically sizes them.',
    long_description=readme(),
    packages=find_packages(),
    install_requires=[
        'sorl-thumbnail',
        'Jinja2',
        'django>=1.11,<1.12',
        'django-jinja>=2.2',
    ],
    extras_require={
        'testing': [
            'coveralls',
            'pytest',
            'pytest-cov',
            'pytest-django',
            'pylint',
            'pylint-django',
            'pylint-mccabe',
            'isort',
        ],
    },
    include_package_data=True,
    url='https://github.com/dan-gamble/django-lazy-image/',
    author='Dan Gamble',
    author_email='dan@dangamble.co.uk',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    },
)
