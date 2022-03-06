.. CBRA documentation master file, created by
   sphinx-quickstart on Mon Mar  7 16:46:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CBRA (Class-based REStful APIs)
===============================
The :mod:`cbra` (pronounced "zebra") package is a framework to create REStful
HTTP APIs using a class-based, object-oriented approach. It is implemented
on top of :mod:`starlette` and :mod:`fastapi`, and draws inspiration from
Django and Django RESt Framework.

Key features
------------
- **Asynchronous:** designed from scratch to support asynchronous I/O in Python
  web applications.
- **Lightning-speed development:** wireframe a REStful web resource by simply
  subclassing :class:`cbra.Resource`.
- **Faster time-to-market:** measured in hours, not weeks.
- **Easy to adopt:** a friendly environment for seasoned Django developers.
- **Built-in support for webhooks and event-driven systems.**

Installation
------------
To install :mod:`cbra` with Python 3.8+:

.. code:: sh

  pip3 install cbra


Getting started
---------------
Head over to the :ref:`Guides<guides>` section to get started!


.. toctree::
   :maxdepth: 2
   :hidden:

   Guides<guides/intro>
   Reference<reference/intro>
