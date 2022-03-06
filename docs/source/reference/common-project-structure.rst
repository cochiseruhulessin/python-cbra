.. _ref-common-project-structure:

=============
Zebra Pattern
=============

This document specifies how a :mod:`cbra` project should be structured.

Overview
========
A well-defined common structure for software projects eases maintenance,
onboarding of new project members and provides a mental framework
to quickly understand how a software application is designed.
The :mod:`cbra` framework comes with a predefined project structure,
that helps developers in quickly getting up to speed with applications
developed using the framework. It provides a conceptual model of how
code should be organizaned, and a well-defined meaning of specific
file- and directory paths.

Core concepts
=============

Layered applications
--------------------
All code is organized in either one of the following categories:

- **Application code:** is the code that implements the application
  layer of a software application. It wires together various concerns
  in order to provide an end-to-end implementation of a use case.
- The **Canonical model** defines datastructures used by all other
  code categories. For larger systems, the canonical model may be
  retained in a separate package.
- A **Domain Layer** is an implementation of pure domain logic.
- The **Infrastructure layer** implements functionality that interacts
  with the infrastructure that supports an application, such as
  databases, mailservers or other external services.
- **Runtime code** is code responsible for setting up and configuring
  the application in a specific environment. Examples of runtime code
  are a settings module, a boot module or a teardown module.
- **Library code** implements utility functions and classes. It must
  not depend on code from any of the other categories.

These categories are implemented as sub-packages of the projects'
top-level package. In a project named ``example``, the paths would
be as defined in the table below:

=================== =================
``example/app``     Application
``example/canon``   Canonical model
``example/domain``  Domain
``example/infra``   Infrastructure
``example/lib``     Library
``example/runtime`` Runtime
=================== =================

Imports between various categories should go from the top-level package of a specific category (the second level of the main package),
e.g. ``from example.infra import SQLBookRepository`` but not
``from example.infra.repo.book import SQLBookRepository``.

Services
--------
A **Service** implements one or more operations without encapsulating
state. Services may be implemented in the application, domain and
infrastructure layer as a Python class. A brief example of such a service is shown below:

.. code:: python

    import typing

    import cbra


    class EmailService:
        """Provides an interface to send email messages to one or
        many recipients.
        """
        __module__: str = 'example.infra.services'

        def __init__(self,
            api_key: str = cbra.Environment('EMAIL_SERVICE_API_KEY')
        ):
            self.api_key

        async def send(self,
            sender: str,
            recipients: typing.List[str],
            subject: str,
            text: str,
            html: typing.Optional[str] = None,
        ):
            # Do something to deliver the email.



Project files and folders
=========================
This section describes the meaning of files and folders in a
project. The assumed working directory is the root folder of the
project.

``Dockerfile``
--------------
For applications that are containerized using Docker, the instruction
to build a Docker image.

``./bin/docker-entrypoint``
---------------------------
If ``Dockerfile`` exists, then this file is the entrypoint for the
Docker image. It must satisfy the following requirements:

- Executable so that ``./bin/docker-entrypoint`` succesfully invokes
  the program (i.e. ensure that there is a propery shebang line).
- The program must accept a positional argument indicating in what
  mode the application should be booted. With regards to the
  :mod:`cbra` framework, this argument is ``runhttp``. If the argument
  is omitted, ``runhttp`` should be assumed.
- It must properly detect and handle the environment variables
  :envvar:`FORWARDED_ALLOW_IPS`, :envvar:`WEB_CONCURRENCY`.

``.dockerignore``
-----------------
The list of files and directories to exclude from the Docker build
context. At least the following paths must be excluded:

.. code::

    ops/*
    .git/*
    .github/*
    .lib/*
    .venv/*


``Makefile``
------------
Implements targets for developing, testing and linting the software.

If present, the ``Makefile`` must implement the following targets:

- ``env`` - Ensure that all dependencies are present, producing a ready-to-serve
  local development environment. This target is idempotent.
- ``runhttp`` - Run a local HTTP server.
- ``test-unit`` - Run all tests marked as unit tests.
- ``test-integration`` - Run all tests marked as integration tests.
- ``test-system`` - Run all tests marked as system tests.

Package files and folders
=========================
This section describes the meaning of files and folders in the main
Python package of a software project. The assumed working directory
is the root folder of the package.

``./__main__.py``
-----------------
The main entrypoint for an application. Invoked using
``{subcommand} (additional parameters)``.

If invoked without any arguments, start the HTTP server with the default
configuration.


``./app``
---------
The top-level package holding the **Application code**. Packages and
modules not under ``./app`` must not imported from anything below
``./app``.

``./app/asgi.py``
-----------------
Declares the ASGI application.

- Must declare an :attr:`application` attribute that holds an instance
  of an ASGI compliant object.

``./app/handlers``
------------------
Holds all implementations of :class:`cbra.CommandHandler`.

``./app/listeners``
-------------------
Holds all implementations of :class:`cbra.EventListener`.

``./app/resources``
-------------------
Holds all implementations of :class:`cbra.Resource`.

``./app/services``
------------------
Holds all application service implementations.

``./app/webhooks``
------------------
Holds all implementations of :class:`cbra.ext.Webhook`.


``./canon(/__init__.py)``
-------------------------
The top-level package holding the **Canonical Model**. Symbols
from all sub-packages are imported to this package. Example:

.. code-block:: python
    :caption: ./canon/__init__.py

    # pylint: skip-file
    from .commands import *
    from .events import *
    from .model import *


``./canon/commands(/__init__.py)``
----------------------------------
Holds all :class:`cbra.Command` definitions. Example:

.. code-block:: python
    :caption: ./canon/commands__init__.py

    # pylint: skip-file
    from .placeorder import PlaceOrder

    __all__ = [
        'PlaceOrder'
    ]

The :attr:`__all__` attribute is mandatory.

``./canon/commands/{classname}.py``
-----------------------------------
Contains classes implementing a command. Example:

.. code-block:: python
    :caption: ./canon/commands/placeorder.py

    """Declares :class:`PlaceOrder`."""
    import typing

    import cbra

    from ..model import OrderItem


    class PlaceOrder(cbra.Command):
        """Contains a request to place an order."""
        supplier__id: int
        billing_party_id: int
        items: typing.List[OrderItem]
        fulfillment_deadline: typing.Optional[int] = None


The filenames must not end with ``command.py``.


``./canon/events(/__init__.py)``
--------------------------------
Holds :class:`cbra.Event` definitions. Example:

.. literalinclude:: ../../../examples/orderapp/orderapp/canon/events/__init__.py
    :caption: ./canon/events/__init__.py


The :attr:`__all__` attribute is mandatory.


``./canon/events/{classname}.py``
---------------------------------
Contains classes implementing a command. Example:

.. literalinclude:: ../../../examples/orderapp/orderapp/canon/events/orderplaced.py
    :caption: ./canon/events/orderplaced.py


The filenames must not end with ``event.py``.


``./canon/models``
------------------
Holds the definitions of datastructures commonly used throughout the
application.

``./infra``
-----------
The top-level package holding the **Infrastructure Layer**. Symbols
from all sub-packages are imported to this package.

``./infra/services``
--------------------
Holds all infrastructure service implementations. Example:

.. code-block:: python
    :caption: ./infra/services/__init__.py

    # pylint: skip-file
    from .email import EmailService


``./infra/services/{classname}.py``
-----------------------------------
Contains classes implementing an infrastructure service.

The filenames must not end with ``service.py``.


``./runtime``
-------------
Top-level module for runtime application configuration.


``./runtime/settings[.py]``
---------------------------
The settings module or package holding the application configuration
settings.

If an :attr:`__all__` member is defined, only the listed symbols are
added to the settings.

See also :ref:`guides-configuration`.

``./runtime/settings/{DEPLOYMENT_ENV}[.py]``
--------------------------------------------
If a package or module is found corresponding to the value of the
environment variable :envvar:`DEPLOYMENT_ENV`, the symbols from
this package or module supersede those defined in the default
settings package, if the name is all uppercase.

If an :attr:`__all__` member is defined, only the listed symbols are
added to the settings.

See also :ref:`guides-configuration`.
