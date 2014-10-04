from plone.app.testing.layers import FunctionalTesting
from Products.CMFPlone.testing import ProductsCMFPloneLayer


class BaseLayer(ProductsCMFPloneLayer):
    def setUpZope(self, app, configurationContext):  # pylint: disable=W0613
        # import plone.app.imaging
        # self.loadZCML(package=plone.app.imaging, name='configure.zcml')
        import experimental.noacquisition
        # self.loadZCML(package=experimental.noacquisition, name='configure.zcml')
        self.loadZCML(package=experimental.noacquisition, name='testing.zcml')


BASE = BaseLayer()


BASE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BASE, ),
    name="experimental.noacquisiton:Functional"
)
