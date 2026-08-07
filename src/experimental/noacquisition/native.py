"""Adapter plugging our config.DRYRUN/logging behaviour into
Products.CMFCore.explicitacquisition, the native implementation of
publication through explicit acquisition.

See https://github.com/zopefoundation/Products.CMFCore/blob/master/src/Products/CMFCore/explicitacquisition.py

Note: the Plone site root needs no dedicated adapter here, it is a
Dexterity content object and already provides IContentish.
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
    same logic, but honours ``config.DRYRUN`` and logs.
    """
    if IPublishableThroughAcquisition.providedBy(context):
        return True
    allowed = context.aq_chain == context.aq_inner.aq_chain
    if not allowed:
        logger.warning("traverse without explicit acquisition object=%r", context)
        if config.DRYRUN:
            return True
    return allowed
