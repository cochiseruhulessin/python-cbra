.. _ref-claims:

======
Claims
======

A *claim* is an assertion, usually in an authentication-related context. This document
lists the claims that are used throughout CBRA and their meanings.


``email``
=========
.. claim:: email

The email address of an entity.

.. warning::

  Do not assume that the email address is valid. Implementation may only make this
  assumption if this claim is accompanied by the :claim:`email_verified` claim.

``email_verified``
==================
.. claim:: email_verified

Indicates if a trusted party verified an email address.


``iat``
=======
.. claim:: iat

Describes when an entity was created.


``iss``
=======
.. claim:: iss

Identifies a claim issuer, such as an OAuth 2.x or OpenID Connect authorization
server.

``sub``
=======
.. claim:: sub

Identifies a Subject in an authentication or an authorization context.
Note that this value only uniquely identifies the Subject in combination
with the :claim:`iss`.

``typ``
=======
.. claim:: typ

Used in a JOSE header to indicate the token type. Types recognized by CBRA are:

* ``session+jwt`` - a JSON Web Token holding claims about a cookie-based web session.