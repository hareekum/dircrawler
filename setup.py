import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# Read dependencies from requirements.txt included in the manifest
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')) as f:
    DEPS = f.read().splitlines()

VERSION = '0.0.1'


class NoseTestCommand(TestCommand):
    # http://fgimian.github.io/blog/2014/04/27/running-nose-tests-with-plugins-using-the-
    # setuptools-test-command/
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests'])


setup(
    name='dircrawler',
    version=VERSION,
    author='Hari Kumar',
    author_email='hari@harikumar.info',
    maintainer='Hari Kumar',
    maintainer_email='hari@harikumar.info',
    description='dircrawl leverages python\'s os.walk and supports a set of operations during '
                'traversal',
    packages=find_packages(),
    install_requires=DEPS,
    include_package_data=True,
    tests_require=['setuptools==30.0.0', 'nose==1.3.7', 'mock==2.0.0', 'pyfakefs==2.9',
                   'freezegun==0.3.7'],
    cmdclass={'test': NoseTestCommand},
    entry_points={
        'console_scripts': [
            'crawl = dircrawler.__main__:main'
        ],
    }
)
