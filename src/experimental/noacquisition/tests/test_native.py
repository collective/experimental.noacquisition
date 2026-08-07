import unittest

try:
    import Products.CMFCore.explicitacquisition  # noqa
except ImportError:
    HAS_NATIVE = False
else:
    HAS_NATIVE = True

if HAS_NATIVE:
    import Acquisition
    from zope.interface import alsoProvides
    from zope.interface import implementer

    from Products.CMFCore.interfaces import IContentish
    from Products.CMFCore.interfaces import IPublishableThroughAcquisition

    from experimental.noacquisition import config
    from experimental.noacquisition import native

    class DummyContainer(Acquisition.Implicit):
        pass

    @implementer(IContentish)
    class DummyContent(Acquisition.Implicit):
        pass


@unittest.skipUnless(
    HAS_NATIVE, "Products.CMFCore.explicitacquisition is not available"
)
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


@unittest.skipUnless(
    HAS_NATIVE, "Products.CMFCore.explicitacquisition is not available"
)
class TestInitializeForcesNativeSupport(unittest.TestCase):
    def test_initialize_enables_native_explicit_acquisition(self):
        import os

        from Products.CMFCore import explicitacquisition
        from experimental.noacquisition import initialize

        previous_skip_pta = explicitacquisition.SKIP_PTA
        previous_env = os.environ.get(explicitacquisition.PTA_ENV_KEY)
        try:
            explicitacquisition.SKIP_PTA = True
            os.environ[explicitacquisition.PTA_ENV_KEY] = "false"

            initialize(None)

            self.assertFalse(explicitacquisition.SKIP_PTA)
            self.assertEqual(os.environ[explicitacquisition.PTA_ENV_KEY], "true")
        finally:
            explicitacquisition.SKIP_PTA = previous_skip_pta
            if previous_env is None:
                os.environ.pop(explicitacquisition.PTA_ENV_KEY, None)
            else:
                os.environ[explicitacquisition.PTA_ENV_KEY] = previous_env
