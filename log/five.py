import sys

__ALL__ = ['PY2', 'PY3', 'str']

# Let's start by defining terms.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    str = str

if PY2:
    str = basestring

basestring = str
