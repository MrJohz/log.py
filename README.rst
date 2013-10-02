======
log.py
======

What?
=====

*log.py* is a logging module for Python that is designed be simple enough for a command-line script, but powerful enough for a complex web app.

Why?
====

The logging module that comes with the standard library isn't brilliant to work with.  It's appropriate for the most simple of use-cases, and the most complex of use-cases, but little in between.  *log.py* borrows a few concepts from *logging*, such as the use of named loggers, and inheritence, but it also adds a few of it's own.

How?
====

Easy.  Just import, instantiate, and log.

.. code:: python

    >>> import log
    >>> logger = log.Logger()
    >>> logger.add_output("stdout")
    >>> logger.log("A simple log message.")
    [2013-07-15 16:25z] INFO: A simple log message.

That's it.  