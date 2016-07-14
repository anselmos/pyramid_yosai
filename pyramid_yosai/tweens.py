
from pyramid.exceptions import ConfigurationError
from yosai.web import WebYosai
from .cookies import PyramidWebRegistry
import pdb

def pyramid_yosai_tween_factory(handler, registry):
    """
    This tween obtains the currently executing subject instance from Yosai and
    makes it available from the request object.
    """

    yosai = registry.get('yosai')
    if yosai is None:
        msg = ('You cannot register the Yosai subject tween without first '
               'registering a yosai instance with Pyramid."')
        raise ConfigurationError(msg)

    def tween(request):
        web_registry = PyramidWebRegistry(request)
        subject = yosai.get_subject(web_registry)
        with WebYosai.context(subject):
            response = handler(request)
        return response

    return tween
