.. _guides-dependency-injection:

====================
Dependency injection
====================


Overview
========
In software engineering, dependency injection is a technique in which an object
receives other objects that it depends on, called dependencies. Typically,
the receiving object is called a client and the passed-in (*injected*) object
is called a service. The code that passes the service to the client is called
the injector. Instead of the client specifying which service it will use, the
injector tells the client what service to use. The 'injection' refers to the
passing of a dependency (a service) into the client that uses it.

The service is made part of the client's state. Passing the service to the
client, rather than allowing the client to build or find the service, is the
fundamental requirement of the pattern.

The intent behind dependency injection is to achieve separation of concerns of
construction and use of objects. This can increase readability and code reuse.

Dependency injection is one form of the broader technique of inversion of control.
A client who wants to call some services should not have to know how to construct
those services. Instead, the client delegates to external code (the injector).
The client is not aware of the injector. The injector passes the services,
which might exist or be constructed by the injector itself, to the client. The
client then uses the services.

This means the client does not need to know about the injector, how to construct
the services, or even which services it is actually using. The client only needs
to know the interfaces of the services, because these define how the client may
use the services. This separates the responsibility of *use* from the
responsibility of *construction* (Wikipedia).

The :mod:`cbra` framework implements dependency injection using *boot-time
dependency injection* and *run-time dependency injection*. The main difference
between these methods is that dependencies injected at boot-time are resolved
from either explicit calls or a configuration file. Run-time depedency
injection on the other hand, is implemented by *inspecting* the signature of
a function or method. Boot-time dependency injection is generally used in the
following cases:

- Configuring classes and factory functions that are not expected to change
  during application run time and do not require dynamic inputs.
- Swapping out a code layer for a mock implementation during testing, for example
  when using the **Repository Pattern**.

Example:

.. literalinclude:: ../../../examples/dependency-injection-simple.py
  :language: python


The depedencies that are injected at boot-time may also be configured through
a settings module, see :attr:`cbra.conf.settings.DEPENDENCIES`.

Run-time dependency injection is more dynamic than injecting at boot-time. It
can inject parameters based on the current HTTP request or dynamically
instantiate the services.

Example:

.. literalinclude:: ../../../examples/dependency-injection-runtime.py
  :language: python


**It is important to note** that the dependencies declared in a function
signature are only injected during certain contexts.

- A request handler that is added to the ASGI application (like the examples
  above).
- In the signature of a dependency that itself is depended upon.
