Changelog
=========

2.0.0b1 (unreleased)
--------------------

- Drop the monkey patches and build on ``Products.CMFCore.explicitacquisition``
  (Products.CMFCore >= 3.1) instead. ``config.DRYRUN`` and logging are kept,
  through an ``IShouldAllowAcquiredItemPublication`` adapter overriding
  CMFCore's own.
  [mamico]

  **Upgrade note:** the native implementation only inspects the last traversed
  object, so acquired content reached *through* a sub-traversing view is no
  longer blocked (``/folder/acquired_image/@@images/image``, restapi services
  taking a subpath). Plain URLs, plain views and plain restapi services are
  still blocked. On Plone 5.2 and 6.0 the ``1.x`` series is still maintained
  and does not have this gap; see README.

- Support Plone 6.0, 6.1 and 6.2 (Python 3.10 - 3.13); drop Plone <= 5.2 and
  Archetypes support, together with the ``collective.monkeypatcher``
  dependency. Plone 5.2 stays on the ``1.x`` branch.
  [mamico]

- Fix Plone 6.2 support: the monkey patch could not even be imported under
  Zope 6 (its ``assert Zope < 6`` fails), so 1.x is unusable there.
  [mamico]

- Depend on ``Products.CMFCore >= 3.1`` instead of ``Zope2``, a distribution
  that no longer exists on Plone 6.1+.
  [mamico]

- Use each Plone release's own bootstrap requirements from
  https://dist.plone.org/release/ , and install ``coverage`` via pip in tox
  instead of through buildout (the buildout egg falls back to the
  pure-python tracer and is much slower on CI).
  [mamico]


1.0.0b10 (2023-02-09)
---------------------

- Zope < 6 (no changes)
  [daniele-andreotti]

1.0.0b9 (2020-07-02)
--------------------

- Zope < 5 (no changes)
  [mamico]

1.0.0b7 (2019-12-10)
--------------------

- Zope < 4.2 (no changes)
  [mamico]


1.0.0b6 (2019-11-07)
--------------------

- Python3 Plone 5.2
  [mamico]


1.0.0b5 (2019-06-05)
--------------------

- Zope2 2.13.28 (no changes)
  [mamico]


1.0.0b4 (2018-05-14)
--------------------

- Zope2 2.13.27 (no changes)
  [mamico]


1.0.0b3 (2017-05-09)
--------------------

- Zope2 2.13.26 (no changes)
  [mamico]

1.0.0b2 (2016-06-10)
--------------------

- Zope2 2.13.24
  [mamico]

1.0.0b1 (2015-10-23)
--------------------

- Zope2 2.13.23 (Plone 4.3.7/5.0)
  [mamico]

1.0.0a5 (2014-10-31)
--------------------

- Nothing changed yet.


1.0.0a4 (2014-10-31)
--------------------

- Initial release
