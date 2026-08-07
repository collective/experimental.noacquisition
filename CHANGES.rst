Changelog
=========

1.0.0b11 (unreleased)
---------------------

- Use ``Products.CMFCore.explicitacquisition`` (Products.CMFCore >= 3.1)
  when available, instead of monkey patching the publisher. Falls back to
  the previous monkey patches on older Zope/CMFCore. Known limitation:
  unlike the monkey patch, the native implementation only catches acquired
  content when the URL resolves directly to it, not when it's reached
  through a view (e.g. an image scale); see README.
  [mamico]

- Add Plone 6.1 and 6.2 to the test matrix, using each release's own
  bootstrap requirements from https://dist.plone.org/release/ (needed on
  Python >= 3.12, where the pip/setuptools pinned for Plone 6.0 crash).
  [mamico]

- Install ``coverage`` via pip in tox instead of through buildout: the
  buildout egg falls back to the pure-python tracer and is much slower
  on CI.
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
