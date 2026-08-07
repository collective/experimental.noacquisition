##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Basic ZPublisher request management.

+ monkeypatch for break traversing without explicit acquisition

"""

import logging
import pkg_resources
from Acquisition import aq_base
from Acquisition.interfaces import IAcquirer
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.interfaces import IPloneSiteRoot
from ZPublisher.interfaces import UseTraversalDefault
from ZPublisher.BaseRequest import typeCheck
from zExceptions import Forbidden
from zExceptions import NotFound
from zope.component import queryMultiAdapter
from zope.interface import Interface

from experimental.noacquisition import config

logger = logging.getLogger("experimental.noacquisition")

# PARANOID VERSION CHECK: publishTraverse() below is a modified copy of
# ZPublisher.BaseRequest.DefaultPublishTraverse.publishTraverse. Bail out
# rather than risk silently diverging from upstream's behaviour on a Zope
# version we haven't checked this copy against. Verified up to Zope 6.1
# (Plone 6.2): its publishTraverse is unchanged since at least Zope 5.13.
_ZOPE_VERSION = pkg_resources.parse_version(
    pkg_resources.get_distribution("Zope").version
)
assert _ZOPE_VERSION < pkg_resources.parse_version("6.2"), (  # noqa: S101
    "experimental.noacquisition's monkey patch has only been verified up "
    "to Zope 6.1 (Plone 6.2). Consider the 2.x series of this package "
    "instead, which builds on Products.CMFCore.explicitacquisition rather "
    "than patching the publisher."
)


def publishTraverse(self, request, name):
    object = self.context
    URL = request["URL"]

    if name[:1] == "_":
        raise Forbidden("Object name begins with an underscore at: %s" % URL)

    subobject = UseTraversalDefault  # indicator
    try:
        if hasattr(object, "__bobo_traverse__"):
            try:
                subobject = object.__bobo_traverse__(request, name)
                if isinstance(subobject, tuple) and len(subobject) > 1:
                    # Add additional parents into the path
                    # XXX There are no tests for this:
                    request["PARENTS"][-1:] = list(subobject[:-1])
                    object, subobject = subobject[-2:]
            except (AttributeError, KeyError, NotFound) as e:
                # Try to find a view
                subobject = queryMultiAdapter((object, request), Interface, name)
                if subobject is not None:
                    # OFS.Application.__bobo_traverse__ calls
                    # REQUEST.RESPONSE.notFoundError which sets the HTTP
                    # status code to 404
                    request.response.setStatus(200)
                    # We don't need to do the docstring security check
                    # for views, so lets skip it and
                    # return the object here.
                    if IAcquirer.providedBy(subobject):
                        subobject = subobject.__of__(object)
                    return subobject
                # No view found. Reraise the error
                # raised by __bobo_traverse__
                raise e
    except UseTraversalDefault:
        pass
    if subobject is UseTraversalDefault:
        # No __bobo_traverse__ or default traversal requested
        # Try with an unacquired attribute:
        if hasattr(aq_base(object), name):
            subobject = getattr(object, name)
        else:
            # We try to fall back to a view:
            subobject = queryMultiAdapter((object, request), Interface, name)
            if subobject is not None:
                if IAcquirer.providedBy(subobject):
                    subobject = subobject.__of__(object)
                return subobject

            # And lastly, of there is no view, try acquired attributes, but
            # only if there is no __bobo_traverse__:
            try:
                subobject = getattr(object, name)
                logger.debug(
                    "traverse without explicit acquisition "
                    "object=%r name=%r subobject=%r url=%r referer=%r",
                    object,
                    name,
                    subobject,
                    request.get("ACTUAL_URL"),
                    request.get("HTTP_REFERER", "-"),
                )
                #
                # STOP TRAVERSING WITHOUT EXPLICIT ACQUISITION
                #
                if IContentish.providedBy(subobject) or IPloneSiteRoot.providedBy(
                    subobject
                ):
                    logger.warning(
                        "traverse without explicit acquisition "
                        "object=%r name=%r subobject=%r url=%r referer=%r",
                        object,
                        name,
                        subobject,
                        request.get("ACTUAL_URL"),
                        request.get("HTTP_REFERER", "-"),
                    )
                    if not config.DRYRUN:
                        subobject = None
                        raise AttributeError
                # Again, clear any error status created by
                # __bobo_traverse__ because we actually found something:
                request.response.setStatus(200)
            except AttributeError:
                pass

            # Lastly we try with key access:
            if subobject is None:
                try:
                    subobject = object[name]
                except TypeError:  # unsubscriptable
                    raise KeyError(name)

    if hasattr(request, "ensure_publishable"):
        # Zope >= 5.10: this also understands the newer @zpublish marker,
        # not just docstring-based publication control.
        request.ensure_publishable(subobject)
    else:
        # Older Zope (e.g. the Zope 4.x that ships with Plone 5.2): fall
        # back to the check request.ensure_publishable() replaced.

        # Check that built-in types aren't publishable.
        if not typeCheck(subobject):
            raise Forbidden("The object at %s is not publishable." % URL)

        # Ensure that the object has a docstring, or that the parent
        # object has a pseudo-docstring for the object. Objects that
        # have an empty or missing docstring are not published.
        doc = getattr(subobject, "__doc__", None)
        if not doc:
            raise Forbidden(
                "The object at %s has an empty or missing "
                "docstring. Objects must have a docstring to be "
                "published." % URL
            )

    return subobject
