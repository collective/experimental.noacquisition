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

Usage
=====

This is a monkey patch for publishTraverse method of Zope2's
``ZPublisher.BaseRequest.DefaultPublishTraverse`` and a monkey patch
for ``Products.Archetypes.BaseObject.BaseObject.__bobo_traverse__``

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

Tests
=====

This add-on is tested using Travis CI. The current status of the add-on is :

.. image:: https://secure.travis-ci.org/collective/experimental.noacquisition.png
    :target: http://travis-ci.org/collective/experimental.noacquisition


Other solutions
===============

There is a more elegant solution in a branch of Products.CMFPlone, that makes use of IPubAfterTraversal event instead of a monkey patch. 
But seems that currently it doesn't works for all cases, at least when there is a custom traversal at the end of the request (take a look at the tests inside this package).
https://github.com/plone/Products.CMFPlone/tree/publication-through-explicit-acquisition

There is also other packages with same approach as CMFPlone's branch:
`collective.explicitacquisition <https://github.com/collective/collective.explicitacquisition>`_ and
`collective.redirectacquired <https://github.com/collective/collective.redirectacquired>`_
