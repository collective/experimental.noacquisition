import importlib
import os
import unittest

import Acquisition
from Products.CMFCore import explicitacquisition
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IPublishableThroughAcquisition
from zope.interface import alsoProvides
from zope.interface import implementer

from experimental.noacquisition import config
from experimental.noacquisition import native


class DummyContainer(Acquisition.Implicit):
    pass


@implementer(IContentish)
class DummyContent(Acquisition.Implicit):
    pass


class TestNativeContentAllowed(unittest.TestCase):
    def setUp(self):
        self._original_dryrun = config.DRYRUN
        config.DRYRUN = False

        self.root = DummyContainer()
        self.other = DummyContainer()
        self.root.content = DummyContent()
        self.root.other = self.other

    def tearDown(self):
        config.DRYRUN = self._original_dryrun

    def test_not_acquired_content_is_allowed(self):
        # Directly contained: aq_chain == aq_inner.aq_chain
        self.assertTrue(native.content_allowed(self.root.content))

    def test_acquired_content_is_not_allowed(self):
        # Reached through "other": acquired, not directly contained
        self.assertFalse(native.content_allowed(self.root.other.content))

    def test_acquired_content_is_logged_but_allowed_in_dryrun(self):
        config.DRYRUN = True
        self.assertTrue(native.content_allowed(self.root.other.content))

    def test_marker_interface_bypasses_the_check(self):
        alsoProvides(self.root.content, IPublishableThroughAcquisition)
        self.assertTrue(native.content_allowed(self.root.other.content))


class TestPackageImportForcesNativeSupport(unittest.TestCase):
    """Importing experimental.noacquisition must force
    Products.CMFCore.explicitacquisition on, even though Plone < 7 ships
    it disabled. This has to happen at module import time, not in
    ``initialize()``: Zope may never call that for a
    five:registerPackage-only package (confirmed: it doesn't, at least
    under plone.app.testing).
    """

    def test_importing_the_package_enables_native_explicit_acquisition(self):
        import experimental.noacquisition

        previous_skip_pta = explicitacquisition.SKIP_PTA
        previous_env = os.environ.get(explicitacquisition.PTA_ENV_KEY)
        try:
            explicitacquisition.SKIP_PTA = True
            os.environ[explicitacquisition.PTA_ENV_KEY] = "false"

            importlib.reload(experimental.noacquisition)

            self.assertFalse(explicitacquisition.SKIP_PTA)
            self.assertEqual(os.environ[explicitacquisition.PTA_ENV_KEY], "true")
        finally:
            explicitacquisition.SKIP_PTA = previous_skip_pta
            if previous_env is None:
                os.environ.pop(explicitacquisition.PTA_ENV_KEY, None)
            else:
                os.environ[explicitacquisition.PTA_ENV_KEY] = previous_env
