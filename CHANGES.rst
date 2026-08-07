Changelog
=========

1.0.0b11 (unreleased)
---------------------

- Support Plone 6.2 (Zope 6.1): raise the paranoid version check from
  ``Zope < 6`` to ``Zope < 6.2`` (verified that
  ``DefaultPublishTraverse.publishTraverse`` is unchanged between Zope 5.13
  and 6.1), and delegate the final publishability check to
  ``request.ensure_publishable()`` when available (Zope >= 5.10), falling
  back to the old docstring/typeCheck logic on older Zope (e.g. Plone 5.2's
  Zope 4.x). ``ensure_publishable`` also understands the newer
  ``@zpublish`` marker, which the previous docstring-only check did not.
  [mamico]

- CI: pin ``zc.buildout = 3.1.0`` for Plone 5.2 (``test-5.2.x.cfg``).
  Plone 5.2's own pin, 3.0.1, has a race-condition bug in
  ``_move_to_eggs_dir_and_compile()`` that raises a bare
  ``AssertionError`` instead of the real error (fixed in 3.1.0, see
  `buildout/buildout#307 <https://github.com/buildout/buildout/issues/307>`_).
  Stayed below 4.0, which requires Python >= 3.9 and would break
  py27/py36/py37/py38.
  [mamico]

- CI: add Plone 6.1 and 6.2 to the test matrix (py310-py313), bootstrapping
  each from its own official ``https://dist.plone.org/release/<x>/requirements.txt``.
  Comment out ``py27-plone52``, ``py37-plone52`` and ``py38-plone60`` (all
  still work with tox locally): ``actions/setup-python`` can no longer
  install Python 2.7/3.7 on the ubuntu-24.04 runner image, and Plone 6.0's
  current constraints pin ``plone.recipe.zope2instance >= 8.0.0``, which
  requires Python >= 3.9. Also set ``fail-fast: false`` so one broken leg
  stops hiding the others.
  [mamico]

- Replace the Bandit security check (broken: its Docker image is based on
  an archived Debian Buster) with ``ruff --select S``, the equivalent
  ruleset. Renamed ``bandit.yml`` to ``sast.yaml``.
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
