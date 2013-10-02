import sys

__ALL__ = ['PY2', 'PY3', 'str']

# Let's start by defining terms.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    str = str

    import io
    cStringIO = StringIO = io.StringIO
    cBytesIO = BytesIO = io.BytesIO

if PY2:
    str = basestring

    import StringIO as _StringIO
    BytesIO = StringIO = _StringIO.StringIO

    try:
        import cStringIO as _cStringIO

    except ImportError:
        cStringIO = StringIO

    else:
        cStringIO = _cStringIO.StringIO

basestring = str
