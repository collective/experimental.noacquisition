import os

from Products.CMFCore import explicitacquisition


# Plone < 7 ships Products.CMFCore.explicitacquisition disabled by default
# (see Products.CMFPlone.__init__), and SKIP_PTA is a module level constant
# computed once at import time, so setting the environment variable alone
# can be too late. Override both, at import time: Zope may never call
# initialize() for a five:registerPackage-only package, and this has to
# happen before any request is published.
explicitacquisition.SKIP_PTA = False
os.environ[explicitacquisition.PTA_ENV_KEY] = "true"


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
