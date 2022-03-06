.. _guides-authentication:

=======================
Authenticating requests
=======================

.. module:: cbra.auth


The :mod:`cbra` module comes with a basic authentication system that enables
resolving an incoming HTTP request to a subject identifier, based on the
parameters included in the request, such as headers or cookies. A subject
identifier uniquely points to an account of some kind (user account, service
account) that has access to certain protected resources.

A simple example is shown below:

.. code:: python

    import cbra
    import cbra.auth


    app = cbra.Application()

    @app.get('/')
    async def hello(principal: cbra.auth.DebugPrincipal = cbra.Depends()):
        return {
            'sub': principal.sub
        }


    if __name__ == '__main__':
        cbra.run('__main__:app', reload=True)



Principal interface
===================
All principal implementations must inherit from :class:`cbra.types.IPrincipal`.
This class specifies the interface that a subclass must implement.


:class:`cbra.types.IPrincipal`
------------------------------

.. autoclass:: cbra.types.IPrincipal

  **Attributes:**

  .. autoattribute:: sub

  **Methods:**

  .. automethod:: is_authenticated()




Principal implementations
=========================

:class:`cbra.auth.DebugPrincipal`
---------------------------------

.. autoclass:: DebugPrincipal

  **Attributes:**

  .. autoattribute:: cookie_name
