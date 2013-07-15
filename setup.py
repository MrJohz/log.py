from distutils.core import setup

setup(
    name='log.py',
    version='0.1.0',
    author='Johz',
    author_email='jonathan.frere@gmail.com',
    packages=['log', 'log.test'],
    url='http://pypi.python.org/pypi/log.py/',
    license='LICENSE.txt',
    description='Simple, clever, Pythonic logging.',
    long_description=open('README.rst').read()
)
