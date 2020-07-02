import logging
from Products.Archetypes.utils import shasattr
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.interfaces import IPloneSiteRoot
from ZPublisher import xmlrpc
from webdav.NullResource import NullResource
from zope.component import queryMultiAdapter
from zope.interface import Interface
from experimental.noacquisition import config


logger = logging.getLogger('experimental.noacquisition')


def __bobo_traverse__(self, REQUEST, name):
    """Allows transparent access to session subobjects.
    """
    # sometimes, the request doesn't have a response, e.g. when
    # PageTemplates traverse through the object path, they pass in
    # a phony request (a dict).

    RESPONSE = getattr(REQUEST, 'RESPONSE', None)

    # Is it a registered sub object
    data = self.getSubObject(name, REQUEST, RESPONSE)
    if data is not None:
        return data
    # Or a standard attribute (maybe acquired...)
    target = None
    method = REQUEST.get('REQUEST_METHOD', 'GET').upper()
    # Logic from "ZPublisher.BaseRequest.BaseRequest.traverse"
    # to check whether this is a browser request
    if (len(REQUEST.get('TraversalRequestNameStack', ())) == 0 and  # NOQA
        not (method in ('GET', 'HEAD', 'POST') and not
             isinstance(RESPONSE, xmlrpc.Response))):
        if shasattr(self, name):
            target = getattr(self, name)
    else:
        if shasattr(self, name):  # attributes of self come first
            target = getattr(self, name)
        else:  # then views
            target = queryMultiAdapter((self, REQUEST), Interface, name)
            if target is not None:
                # We don't return the view, we raise an
                # AttributeError instead (below)
                target = None
            else:  # then acquired attributes
                target = getattr(self, name, None)
                if target is not None:
                    logger.debug(
                        'traverse without explicit acquisition '
                        'object=%r name=%r subobject=%r url=%r referer=%r',
                        self, name, target,
                        REQUEST.get('ACTUAL_URL'),
                        REQUEST.get('HTTP_REFERER', '-')
                    )
                    #
                    # STOP TRAVERSING WITHOUT EXPLICIT ACQUISITION
                    #
                    if REQUEST.get('ACTUAL_URL') and (
                            IContentish.providedBy(target) or  # NOQA
                            IPloneSiteRoot.providedBy(target)):
                        logger.warning(
                            'traverse without explicit acquisition '
                            'object=%r name=%r subobject=%r url=%r referer=%r',
                            self, name, target,
                            REQUEST.get('ACTUAL_URL'),
                            REQUEST.get('HTTP_REFERER', '-')
                        )
                        if not config.DRYRUN:
                            target = None

    if target is not None:
        return target
    elif (method not in ('GET', 'POST') and not
          isinstance(RESPONSE, xmlrpc.Response) and  # NOQA
          REQUEST.maybe_webdav_client):
        return NullResource(self, name, REQUEST).__of__(self)
    else:
        # Raising AttributeError will look up views for us
        raise AttributeError(name)
