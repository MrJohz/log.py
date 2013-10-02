import datetime
import sys
from threading import Lock

from . import five

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S%z"
DEFAULT_FORMAT = "[{datetime}] {level}: {message}"
DEFAULT_LEVEL = "INFO"
NEWLINE = '\n'

LEVELS = {"NOTSET":   00,
          "DEBUG":    10,
          "INFO":     20,
          "NOTICE":   25,
          "WARNING":  30,
          "ERROR":    40,
          "CRITICAL": 50}

## HELPER FUNCTIONS


def _isiterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def _get_list(obj):
    if _isiterable(obj):
        return list(obj)
    else:
        return [obj]


def _if_none(obj, func, sentinel=None):
    return func() if obj is sentinel else obj


## FUNCTIONS

def level(level):
    level = LEVELS.get(level, level)

    def filter_func(msg_level):
        msg_level = LEVELS.get(msg_level, msg_level)
        if msg_level >= level:
            return True
        else:
            return False
    return filter_func


## Output
class Output(object):
    def __init__(self, output, **kwargs):

        # Set self.output
        if output in ['stdin', 'stdout', 'stderr']:  # Catch these seperately
            self.output = getattr(sys, output)
        elif isinstance(output, five.str):           # Gave filename
            self.output = open(output, kwargs.get("filemode", 'a'))
        else:                                        # Gave some filetype
            self.output = output

        # Set self.filters
        filtr = kwargs.get("filter")
        self.filters = [] if filtr is None else [filtr]

        filter_funcs = kwargs.get("filters", list())
        self.filters.extend(filter_funcs)

        # If a message has no tags, should we accept it?
        self.accept_empty = kwargs.get("accept_empty", True)

        # Set self.level
        self.level = kwargs.get("level", level(DEFAULT_LEVEL)) # fix this

        self.format = kwargs.get('format', DEFAULT_FORMAT)
        self.date_fmt = kwargs.get('date_fmt', DEFAULT_DATE_FORMAT)
        if 'formatter' in kwargs:
            self.formatter = kwargs['formatter']

    def check_valid(self, message):
        """A check to see if `message` should be written by this Output."""
        if (not message.tags) and not self.filters:
            return True

        true_results = list()
        for filtr in self.filters:
            if not filtr(message):
                return False

        return True

    def formatter(self, message):
        time_string = message.datetime.strftime(self.date_fmt)
        args = message.args()
        args.update(datetime=time_string)
        return self.format.format(**args)

    def write(self, message):
        """Writes `message` to `self.output`"""
        self.output.write(self.formatter(message))
        self.output.write(NEWLINE)
        try:
            self.output.flush()
        except:
            pass


class Message(object):
    def __init__(self, message, level=DEFAULT_LEVEL,
                 tags=None, args=None, kwargs=None):
        self.tags = _get_list(_if_none(tags, list))
        self.raw_message = message
        args = _if_none(args, list)
        kwargs = _if_none(kwargs, dict)
        self.message = message.format(*args, **kwargs)
        self.level = level
        self.datetime = datetime.datetime.today()

    def args(self):
        return {'tags': self.tags,
                'message': self.message,
                'level': self.level,
                'datetime': self.datetime}

    def __str__(self):
        return "<{clname} {message!r}>".format(clname = self.__class__.__name__, message=self.message)

    __repr__ = __str__


class Logger(object):

    instances = {}

    def __new__(cls, name='root', *args, **kwargs):
        if name in cls.instances:
            return cls.instances[name]

        else:
            new = object.__new__(cls, *args, **kwargs)
            new.name = name
            cls.instances[name] = new
            return new

    def __init__(self, name="root", **kwargs):
        if hasattr(self, 'outputs'):
            self.outputs.extend(_get_list(kwargs.get("outputs", [])))
        else:
            self.outputs = _get_list(kwargs.get("outputs", []))

        self.outputs.append(kwargs.get('output'))

        self.lock = Lock()

    def add_outputs(self, *outputs):
        self.outputs.extend(outputs)

    def add_output(self, output):
        self.outputs.append(output)

    def _log(self, message, level, tags, args, kwargs):
        message = Message(message, tags, level, args, kwargs)
        for output in self.outputs:
            if output.check_valid(message):
                output.write(message)

    def log(self, message, level=DEFAULT_LEVEL, tags=None, *args, **kwargs):
        return self._log(message, level, tags, args, kwargs)

    def debug(self, message, tags=None, *args, **kwargs):
        return self._log(message, "DEBUG", tags, args, kwargs)

    def info(self, message, tags=None, *args, **kwargs):
        return self._log(message, "INFO", tags, args, kwargs)

    def notice(self, message, tags=None, *args, **kwargs):
        return self._log(message, "NOTICE", tags, args, kwargs)

    def warning(self, message, tags=None, *args, **kwargs):
        return self._log(message, "WARNING", tags, args, kwargs)

    def error(self, message, tags=None, *args, **kwargs):
        return self._log(message, "ERROR", tags, args, kwargs)

    def critical(self, message, tags=None, *args, **kwargs):
        return self._log(message, "CRITICAL", tags, args, kwargs)
