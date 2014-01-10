import base64
import json
import requests
import magic

from pylons import config
from adhocracy import i18n


class RESTAPI(object):
    """Helper to work with the adhocarcy_service rest api
       (adhocracy_kotti.mediacenter, adhocracy_kotti.staticpages..).
    """

    session = requests.Session()
    """requests http connection object"""

    #TODO make this a method
    images_get, images_post, images_delete = None, None, None
    """requests prepared requests to call /images"""

    def __init__(self):
        self.api_token = config.get('adhocracy_service.rest_api_token', '')
        self.api_address = config.get('adhocracy_service.rest_api_address', '')
        self.headers = {"X-API-Token": self.api_token}
        self.images_get = requests.Request("GET",
                                           url=self.api_address + "images",
                                           headers=self.headers)
        self.images_post = requests.Request("POST",
                                            url=self.api_address + "images",
                                            headers=self.headers)
        self.images_delete = requests.Request("DELETE",
                                              url=self.api_address + "images",
                                              headers=self.headers)

    def staticpages_get(self, base=None, languages=None):
        if languages is None:
            languages = i18n.all_languages(include_preferences=True)
        params = {
            'lang': languages
        }
        if base is not None:
            params['base'] = base
        request = requests.Request("GET",
                                   url='%s%s' % (
                                       self.api_address,
                                       "staticpages",
                                   ),
                                   params=params,
                                   headers=self.headers)

        return self.session.send(request.prepare())

    def staticpage_get(self, path, languages=None):
        if languages is None:
            languages = i18n.all_languages(include_preferences=True)
        request = requests.Request("GET",
                                   url='%s%s' % (
                                       self.api_address,
                                       'staticpages/single',
                                   ),
                                   params={
                                       'path': path,
                                       'lang': languages,
                                   },
                                   headers=self.headers)

        return self.session.send(request.prepare())

    def add_image(self, filename, binarydata):
        """Post image data to the mediacenter

            returns requests response object
        """
        mimetype = magic.from_buffer(binarydata, mime=True)
        image_encoded = base64.b64encode(binarydata)
        request = self.images_post
        request.data = json.dumps(dict(filename=filename,
                                       data=image_encoded,
                                       mimetype=mimetype,
                                       ))
        return self.session.send(request.prepare())
