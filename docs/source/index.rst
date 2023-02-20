.. CBRA documentation master file, created by
   sphinx-quickstart on Mon Mar  7 16:46:40 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CBRA (Class-based REStful API)
==============================
The :mod:`cbra` (pronounced "zebra") package is a framework to create REStful
HTTP APIs using a class-based, object-oriented approach. It is implemented
on top of :mod:`starlette` and :mod:`fastapi`, and draws inspiration from
Django and Django REST Framework.

Key features
------------
- **Asynchronous:** designed from scratch to support asynchronous I/O in Python
  web applications.
- **Lightning-speed development:** wireframe a REStful web resource by simply
  subclassing :class:`cbra.core.ResourceModel`.
- **Faster time-to-market:** measured in hours, not weeks.
- **Easy to adopt:** built on top of FastAPI and Starlette. If you're familiar
  with Django REST Framework, adopting :mod:`cbra` is a small step for you,
  but a giant leap for your project.
- **Built-in support for webhooks and event-driven systems.**
- **All FastAPI benefits plus a class-oriented programming interface.**

Installation
------------
To install :mod:`cbra` with Python 3.10+:

.. code:: sh

  pip3 install cbra


Getting started
===============
Check out the example below to get an idea of :mod:`cbra` and its powerful,
yet simple interface. For all examples, head over to the :ref:`Guides<guides>`
section to get started!


Define your resource model
--------------------------
Implementing a REStful API with :mod:`cbra` always starts with declaratively
defining your resource model.

.. code:: python

  import pydantic
  from cbra.core import ResourceModel


  class Book(ResourceModel):
      # Note the 'primary_key' and 'read_only' arguments. The 'primary_key'
      # argument specifies that this field identifies the Book. The 'read_only'
      # argument indicates that the field may not be set by clients, and
      # will not be ignored in POST/PUT/PATCH requests. It is also not included
      # in the OpenAPI documentation for these methods.
      #
      # When constructing URLs for Resource implementations, this field is used
      # to construct the URL parameter by lowercasing the resource models' name
      # and appending '_id' to it. In this example that would thus be 'book_id'.
      id: int | None = pydantic.Field(
          default=None,
          primary_key=True,
          read_only=True
      )
      title: str


Implementing your resource
--------------------------
To implement endpoints for the :class:`Book` model you defined, create a
subclass of :class:`~cbra.core.Resource` and implement just four methods
to have a fully functional, readable and writable RESTful HTTP resource.

.. code:: python

    import secrets
    from cbra.core import Mutable, Resource


    class BookResource(Resource, Mutable, model=Book):
        books: dict[int, Book] = {
            1: Book(id=1, title="The Hitchhiker's Guide to the Galaxy")
        }

        async def can_create(self, resource: Book) -> bool:
            # Hook to determine if an object can be created. The default
            # implementation always raises a NotImplementedError. Uniqueness
            # check etc. should be performed here.
            return not any([
                x.title == resource.title
                for x in self.books.values()]
            )

        async def delete(self, resource: Book):
            # Delete a resource from your storage backend.  For this example we use
            # a simple dictionary, but in a real implementation this could be
            # a relational database or document storage system.
            assert resource.id is not None
            self.books.pop(resource.id)

        async def get_object(self) -> Book | None:
            # Must be implemented to return an instance of Book, or None
            # if the Book does not exist. In the latter case, the client
            # automatically receives a 404 status code.
            return self.books.get(int(self.request.path_params['book_id']))

        async def persist(self, resource: Book, create: bool = False) -> Book:
            # Persist a resource to your storage backend. Same applies as for
            # delete().
            if create:
                assert resource.id is None
                resource.id = secrets.choice(range(1000, 9999))
            assert resource.id is not None
            self.books[resource.id] = resource
            return resource


Serving your REStful HTTP API
-----------------------------
Exposing :class:`BookResource` to HTTP clients then becomes as simple as:

.. code:: python

    import uvicorn
    import cbra.core as cbra

    app: cbra.Application = cbra.Application()
    app.add(BookResource)

    uvicorn.run(app)

Run this code and visit http://localhost:8000/redoc to see the result! ReDoc
will properly show the exposed GET, POST, PUT, PATCH and DELETE methods. It's
*that* simple.


.. toctree::
   :maxdepth: 2
   :hidden:

   Guides<guides/intro>
   Reference<reference/intro>
