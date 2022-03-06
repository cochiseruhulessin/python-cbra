.. _guides-oauth2:


========================================================
Building OAuth 2.0/Open ID Connect authorization servers
========================================================

The :mod:`cbra` framework provides the core building blocks to implement OAuth
2.0 and OpenID Connect servers and clients.


Resource owner authentication
=============================
Regarding the subject of authentication at the :term:`Authorization Endpoint`,
:rfc:`6749` states:

    The authorization endpoint is used to interact with the resource owner and
    obtain an authorization grant.  The authorization server MUST first verify
    the identity of the resource owner.  The way in which the authorization
    server authenticates the resource owner (e.g., username and password login,
    session cookies) is beyond the scope of this specification.


Glossary
========


.. glossary::

    Authorization Endpoint
        An endpoint exposed by the authorization server that
        is used to interact with the resource owner and obtain
        an authorization grant.


Additional resources
====================
- :rfc:`6749` - The OAuth 2.0 Authorization Framework
- :rfc:`6750` - Bearer Token Usage
- :rfc:`7636` - PKCE: Proof Key for Code Exchange
- :rfc:`6819` - Threat Model and Security Considerations
- :rfc:`7009` - Token Revocation
- :rfc:`7521` - Assertion Framework
- :rfc:`7522` - SAML Assertions
- :rfc:`7523` - JWT Profile for Client Authentication
- :rfc:`7662` - Token Introspection
- :rfc:`8414` - OAuth 2.0 Authorization Server Metadata
- :rfc:`8628` - OAuth 2.0 Device Authorization Grant
- :rfc:`8693` - OAuth 2.0 Token Exchange
- :rfc:`8705` - Mutual TLS Bound Access Tokens
- :rfc:`8707` - Resource Indicators for OAuth 2.0
- :rfc:`9068` - JWT Profile for OAuth Access Tokens
- :rfc:`9101` - The OAuth 2.0 Authorization Framework: JWT-Secured Authorization Request (JAR)
- :rfc:`9126` - OAuth 2.0 Pushed Authorization Requests
- :rfc:`9207` - OAuth 2.0 Authorization Server Issuer Identification
- `OpenID Connect Core 1.0 <https://openid.net/specs/openid-connect-core-1_0.html>`_
- `OpenID Connect Discovery 1.0 <https://openid.net/specs/openid-connect-discovery-1_0-29.html>`_
- `OAuth 2.0 Multiple Response Type Encoding Practices <https://openid.net/specs/oauth-v2-multiple-response-types-1_0.html>`_
- `Financial-grade API Security Profile 1.0 - Part 1: Baseline <https://openid.net/specs/openid-financial-api-part-1-1_0.html>`_
- `Financial-grade API Security Profile 1.0 - Part 2: Advanced <https://openid.net/specs/openid-financial-api-part-2-1_0.html>`_
