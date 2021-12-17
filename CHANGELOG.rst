Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: text

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

0.2.13
------
2021-12-17

- Tested against Django 4.0.

0.2.12
------
2021-12-06

- Tested against Django 3.1 and 3.2.
- Tested against Python 3.9 and 3.10.
- Tested against Django REST Framework 3.12.
- Drop Python 2.x support.
- Drop Python 3.5 support.
- Drop Django < 2.2 support.
- Drop Django REST Framework < 3.9 support.

0.2.11
------
2019-12-27

- Tested against Django 3.0.
- Tested against Python 3.8.
- Tested against Django REST Framework 3.11.

0.2.10
------
2019-04-12

- Tested against Django 2.1 and Django 2.2.
- Tested against Python 3.7.
- Dropping support for Python 3.4.
- Upgrade test suite.
- Temporary remove PyPy from tox (because of failing tests).

0.2.9
-----
2018-02-03

- Make it possible to order by two (or more fields) at once, using the
  ``OrderingFilter``.

0.2.8
-----
2018-01-31

- Fixes in docs.

0.2.7
-----
2018-01-28

- Fixes in docs.

0.2.6
-----
2018-01-28

- Added ``OrderingFilter``, which makes it possible to specify
  mapping (ordering option -> ORM field) for making more developer
  friendly ordering options in the API. An example of such could be
  a ``Profile`` model with ``ForeignKey`` relation to ``User`` model. In
  case if we want to order by ``email`` field in the ``ProfileViewSet``,
  instead of ordering on ``user__email`` we could order just on ``email``.

0.2.5
-----
2017-12-30

- Update example project (and the tests that are dependant on the example
  project) to work with Django 2.0.

0.2.4
-----
2017-07-14

- Fix issue #1 with non-required nested serializer fields.

0.2.3
-----
2017-07-13

- More tests.
- Made tests DRY.

0.2.2
-----
2017-07-04

- Documentation improvements.
- Tested against various Django REST framework versions (>=3.5.0,<=3.6.3).

0.2.1
-----
2017-07-04

- Minor fixes.
- Documentation improvements.

0.2
---
2017-07-02

- Handle unlimited nesting depth for nested serializers of non-relational
  fields.
- Documentation improvements.

0.1.8
-----
2017-07-01

- Initial beta release.
