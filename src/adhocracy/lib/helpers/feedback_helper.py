from paste.deploy.converters import asbool
from adhocracy import config
from adhocracy import model
from adhocracy.lib.helpers import site_helper as _site


def is_configured():
    configured = config.get_bool('adhocracy.use_feedback_instance')
    if not configured:
        return False
    return get_feedback_instance() is not None


def get_feedback_instance():
    return model.Instance.find(config.get('adhocracy.feedback_instance_key',
                                          u'feedback'))


def get_categories():
    feedback_instance = get_feedback_instance()
    return model.CategoryBadge.all(feedback_instance, include_global=False)


def get_proposal_url():
    return _site.base_url(u'/proposal', get_feedback_instance())
