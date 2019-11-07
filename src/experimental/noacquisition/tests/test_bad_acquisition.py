# mostly grabbed from
# https://github.com/plone/Products.CMFPlone/blob/publication-through-explicit-acquisition/Products/CMFPlone/tests/test_bad_acquisition.py

import pkg_resources
import os.path
from six.moves.urllib.error import HTTPError
import unittest
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_PACONTENTTYPES = False
else:
    HAS_PACONTENTTYPES = True

from experimental.noacquisition.testing import BASE_FUNCTIONAL_TESTING
from experimental.noacquisition import config


def dummy_image():
    filename = os.path.join(os.path.dirname(__file__), u'image.gif')
    if HAS_PACONTENTTYPES:
        from plone.namedfile.file import NamedBlobImage
        return NamedBlobImage(
            data=open(filename, 'rb').read(),
            filename=filename
        )
    else:
        return open(filename, 'rb').read()


class TestBadAcquisition(unittest.TestCase):

    layer = BASE_FUNCTIONAL_TESTING

    def setUp(self):
        self.default_dryrun_config = config.DRYRUN
        config.DRYRUN = False
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.portal.invokeFactory('Document', 'a_page')
        self.assertTrue('a_page' in self.portal.objectIds())
        self.portal.invokeFactory('Folder', 'a_folder')
        self.assertTrue('a_folder' in self.portal.objectIds())
        self.portal.invokeFactory('Image', id='a_image', image=dummy_image())
        self.assertTrue('a_image' in self.portal.objectIds())
        import transaction
        transaction.commit()
        self.browser = Browser(self.app)
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,)
        )

    def tearDown(self):
        config.DRYRUN = self.default_dryrun_config

    def test_not_found_when_acquired_content(self):
        self.browser.open(self.portal.a_page.absolute_url())
        error = None
        try:
            url = self.portal.absolute_url() + '/a_folder/a_page'
            self.browser.open(url)
        except HTTPError as e:
            error = e
        self.assertTrue(
            error is not None,
            msg='Acquired content should not be published.')
        self.assertEqual(404, error.code)

    def test_not_found_when_acquired_image_traverser(self):
        url = self.portal.a_image.absolute_url() + "/@@images/image"
        self.browser.open(url)
        error = None
        try:
            url = self.portal.absolute_url() + \
                '/a_folder/a_image/@@images/image'
            self.browser.open(url)
        except HTTPError as e:
            error = e
        self.assertTrue(
            error is not None,
            msg='Acquired content should not be published.')
        self.assertEqual(404, error.code)

    # This currently fails, because p.a.testeing create de plonesite with
    # "plone" id but there is also a view with same name ....
    # def test_not_found_when_acquired_siteroot_1(self):
    #     error = None
    #     try:
    #         url = self.portal.absolute_url() + "/" + self.portal.getId()
    #         self.browser.open(url)
    #     except HTTPError, e:
    #         error = e
    #     self.assertTrue(
    #         error is not None,
    #         msg='Acquired content should not be published.')
    #     self.assertEqual(404, error.code)

    # This currently fails, because p.a.testeing create de plonesite with
    # "plone" id but there is also a view with same name ....
    # def test_not_found_when_acquired_siteroot_2(self):
    #     error = None
    #     try:
    #         url = self.portal.a_folder.absolute_url() + "/" + self.portal.getId()
    #         self.browser.open(url)
    #     except HTTPError, e:
    #         error = e
    #     self.assertTrue(
    #         error is not None,
    #         msg='Acquired content should not be published.')
    #     self.assertEqual(404, error.code)

    # TODO: unfinshed
    # def test_traverse_vhm(self):
    #     url = "http://nohost/VirtualHostBase/http/example.org:80/plone" + \
    #         "/VirtualHostRoot/a_page"
    #     self.browser.open(url)

    def test_traverse_portal_skin_object(self):
        url = self.portal.absolute_url() + '/logo.png'
        self.browser.open(url)
        url = self.portal.a_page.absolute_url() + '/logo.png'
        self.browser.open(url)
        url = self.portal.a_image.absolute_url() + '/logo.png'
        self.browser.open(url)
