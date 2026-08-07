"""Adapter used when Products.CMFCore.explicitacquisition is available
(Products.CMFCore >= 3.1), to plug our config.DRYRUN/logging behaviour
into the native, event based, implementation.

See https://github.com/zopefoundation/Products.CMFCore/blob/master/src/Products/CMFCore/explicitacquisition.py

Note: the Plone site root doesn't need a dedicated adapter here, unlike
the legacy monkey patch: on any Plone new enough to ship
Products.CMFCore >= 3.1, the site root is a Dexterity content object and
already provides IContentish, so it's covered by ``content_allowed``.
"""

import logging

from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IPublishableThroughAcquisition
from zope.component import adapter

from experimental.noacquisition import config

logger = logging.getLogger("experimental.noacquisition")


@adapter(IContentish)
def content_allowed(context):
    """Overrides Products.CMFCore.explicitacquisition.content_allowed:
    same logic, but honours ``config.DRYRUN`` and logs like the legacy
    monkey patch used to.
    """
    if IPublishableThroughAcquisition.providedBy(context):
        return True
    allowed = context.aq_chain == context.aq_inner.aq_chain
    if not allowed:
        logger.warning("traverse without explicit acquisition object=%r", context)
        if config.DRYRUN:
            return True
    return allowed
