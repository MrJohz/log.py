======
log.py
======

What?
=====

*log.py* is a logging module for Python that is designed be simple enough for a command-line script, but powerful enough for a complex web app.

Why?
====

The logging module that comes with the standard library is horrible.  It's appropriate for the most simple of use-cases, and the most complex of use-cases, but little in between.

How?
====

Easy.  Just import, instantiate, and log.

.. code:: python
    import log

    logger = log.Logger()

    logger.add_output("stdout")

    logger.log("A simple log message.")
