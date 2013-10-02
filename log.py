import datetime
import sys
from threading import Lock

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
        elif isinstance(output, basestring):            # Gave filename
            self.output = open(output, kwargs.get("filemode", 'a'))
        else:                                        # Gave some filetype
            self.output = output

        # Set self.filters
        filter_func = kwargs.get("filter", lambda tag: True)
        self.filters = _get_list(filter_func)

        filter_funcs = kwargs.get("filters", list())
        self.filters.extend(filter_funcs)

        # Set self.level
        self.level = kwargs.get("level", level(DEFAULT_LEVEL))

    def check_valid(self, message):
        """A check to see if `message` should be written by this Output."""
        true_tags = list()
        for tag in message.tags:
            for filter_func in self.filters:
                if not filter_func(tag):
                    break
            else:
                true_tags.append(True)

        if self.level(message.level):
            return any(true_tags)

    def write(self, message):
        """Writes `message` to `self.output`"""
        self.output.write(message.line())
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


class Logger(object):

    instances = {}

    def __new__(cls, name="root", *args, **kwargs):
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
