import os

try:
    from Products.CMFCore import explicitacquisition
except ImportError:
    # Products.CMFCore < 3.1: no native support, the monkey patches
    # registered in configure.zcml take care of everything.
    pass
else:
    # Plone < 7 disables this by default (see Products.CMFPlone.__init__),
    # and in any case SKIP_PTA is a module level constant computed once at
    # import time: just setting the environment variable can be too late
    # if something already imported the module, so also override it
    # directly. This must happen at import time (not in initialize(),
    # below, which Zope may never call for a five:registerPackage-only
    # package) so it runs before any request is published.
    explicitacquisition.SKIP_PTA = False
    os.environ[explicitacquisition.PTA_ENV_KEY] = "true"


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
