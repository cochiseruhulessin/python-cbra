.. _guides-integrating-an-existing-fastapi-application:

===============
Getting started
===============

The :mod:`cbra` framework is designed to build fully-asynchronous HTTP server
applications that expose interfaces intended for consumption by computer
programs or system-to-system communication, such as REStful application
programming interfaces, HTTP based command handlers or event listeners, or
webhook receivers.

From scratch
============
Creating a skeleton application is as simple as creating a :class:`cbra.Application`
instance and running it with an ASGI-compliant application server, such as
:mod:`gunicorn` or :mod:`uvicorn`. For conveniance and additional integration
with :mod:`cbra`, the framework comes with a :mod:`uvicorn` implementation that
will be used throughout these guides, an is invoked using :func:`cbra.run`:


.. literalinclude:: ../../../examples/skeleton.py
  :language: python


An instance of :class:`cbra.Application` exposes an interface compliant with the
ASGI standard.

For more control over the behavior of the application, :class:`cbra.Application`
may also be subclassed. Override one or more methods described below to
customize the behavior of the ASGI application:


.. class:: cbra.Application
  :noindex:

  .. automethod:: boot

  .. automethod:: teardown
