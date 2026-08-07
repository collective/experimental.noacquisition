.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://img.shields.io/pypi/v/experimental.noacquisition.svg
    :target: https://pypi.org/project/experimental.noacquisition/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/experimental.noacquisition.svg?style=plastic
    :target: https://pypi.org/project/experimental.noacquisition/
    :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/dm/experimental.noacquisition.svg
    :target: https://pypi.org/project/experimental.noacquisition/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/l/experimental.noacquisition.svg
    :target: https://pypi.org/project/experimental.noacquisition/
    :alt: License

.. image:: https://github.com/collective/experimental.noacquisition/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/collective/experimental.noacquisition/actions
    :alt: Tests

.. image:: https://coveralls.io/repos/github/collective/experimental.noacquisition/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/experimental.noacquisition?branch=master
    :alt: Coverage



Introduction
============

The problem with “acquisition” and publishTraverse is that the current method returns too many different URLs for the same content. 
For instance here is some potential url for the “kb” page of the plone.org website

- https://plone.org/documentation/kb
- https://plone.org/documentation/manual/kb
- https://plone.org/documentation/kb/manual/kb
- https://plone.org/documentation/manual/spinner.gif/kb
- ...

and here is a generic "Plone" site with two content items "a" and "b" (folderish or not)

- http://example.com/Plone/a
- http://example.com/Plone/a/b/a
- http://example.com/Plone/a
- http://example.com/Plone/b/a
- ...

All the urls above returns 200 with the same content, 
while I would like the "canonical url" to return 200 and the other to return 404.

The behaviour described above constitute a problem because:

* multiple url for the same content is a problem for SEO and is confusing to people. 
  For SEO, in the latest versions Plone introduced the canonical META,
  but IMHO it's just a workaround. 
  People are confused. 
  For example: sometimes some of my editors ask me: 
  "I can't remove the http://example.com/Plone/a/b/a/page. Can you do it for me?"

* the page doesn’t seem really the same on all urls: 
  if you open
  https://plone.org/documentation/kb and
  https://plone.org/documentation/manual/kb the second has a portlet that the first is missing

* removing page from external cache (varnish or squid), for example after a
  content modification, will be a pain. 
  This is because for the same content there could be multiple urls without any control or rules 
  (``collective.purgebyid`` solves this)

* when using subsite (or multiple plone site on the same zope app) the problem is even more annoying: 
  suppose that "a" is a subsite (marked with INavigationRoot) for http://a.example.org and "b" for http://b.example.org.
  Opening the url http://a.example.org/b will probably show the homepage of site "a" inside the "b" site.
  ``collective.siteisolation`` and probably ``collective.lineage`` do something to isolate subsite, 
  but IMHO again are only workarounds.

Versions
========

============ =================== ==============================================
Series       Plone               Implementation
============ =================== ==============================================
``2.x``      6.0, 6.1, 6.2       ``Products.CMFCore.explicitacquisition``
``1.x``      5.2, 6.0            monkey patch (maintained on the ``1.x`` branch)
============ =================== ==============================================

``2.x`` is **required** on Plone 6.2: the ``1.x`` monkey patch cannot even be
imported under Zope 6, since it asserts ``Zope < 6``.

``1.x`` is still worth using on Plone 5.2 and 6.0, because it catches one case
that ``2.x`` does not -- see `Known limitation`_ below.

Usage
=====

``Products.CMFCore`` >= 3.1 (i.e. Plone 6) ships a native implementation of
this same idea, based on the ``IPubAfterTraversal`` event instead of monkey
patching the publisher: see
`explicitacquisition.py <https://github.com/zopefoundation/Products.CMFCore/blob/master/src/Products/CMFCore/explicitacquisition.py>`_.
This package builds on it:

* ``Products.CMFCore.explicitacquisition`` is force-enabled, since Plone < 7
  disables it by default (see
  `Products.CMFPlone #3781 <https://github.com/plone/Products.CMFPlone/pull/3781>`_);
* an adapter for ``IShouldAllowAcquiredItemPublication`` is registered in
  place of CMFCore's default one, adding ``config.DRYRUN`` and logging.

Known limitation
----------------

``Products.CMFCore.explicitacquisition`` only inspects the *last* traversed
object (``PARENTS[0]``). When traversal continues **through** a view that
consumes further path segments, that view -- not the acquired content --
ends up being the object inspected, so the acquired content goes unnoticed
and is served.

Confirmed cases::

    /folder/acquired_image/@@images/image          served (should be 404)
    /folder/acquired_doc/@types/Document           served (should be 404)
    /folder/acquired_doc/@vocabularies/<name>      served (should be 404)

Plain URLs, plain views (``/edit``, ``@@edit``) and plain ``plone.restapi``
services (``@breadcrumbs``, ``@navigation``, ...) *are* correctly blocked.

This is a limitation of the upstream implementation, not something this
package can work around; ``test_not_found_when_acquired_image_traverser`` is
marked as an expected failure for this reason. The ``1.x`` monkey patch does
not have this gap, because it checks at *every* traversal step instead of
only at the end -- so on Plone 5.2 and 6.0, where ``1.x`` still works,
staying on ``1.x`` gives full coverage.

By default invalid traverse is only logged as warning.

For enable raising exceptions, you need to manually modify ``config.py`` changing ``DRYRUN`` to ``False``. 

Or using ``plone.recipe.zope2instance >= 4.2.14``, e.g.::

    [instance]
    recipe = plone.recipe.zope2instance
    eggs =
        experimental.noacquisition
    ...
    initialization =
       from experimental.noacquisition import config
       config.DRYRUN = False


Warning
=======

**USE AT YOUR OWN RISK**

Don't use it, if you don't know exactly what are you doing... at least use leaving ``DRYRUN = True``.


Other solutions
===============

The ``Products.CMFPlone`` branch that used to be linked here, based on the
``IPubAfterTraversal`` event instead of a monkey patch, eventually got
merged into ``Products.CMFCore`` itself (3.1+) as
``Products.CMFCore.explicitacquisition``. Since 2.0 this package builds on
it directly, see `Usage`_ above.

There is also other packages with a similar, event based, approach:
`collective.explicitacquisition <https://github.com/collective/collective.explicitacquisition>`_ and
`collective.redirectacquired <https://github.com/collective/collective.redirectacquired>`_
