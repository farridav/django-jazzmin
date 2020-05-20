import logging
from urllib.parse import urlencode

from django.db.models.base import ModelBase

from jazzmin.compat import reverse, NoReverseMatch

logger = logging.getLogger(__name__)


def order_with_respect_to(first, reference):
    ranking = []
    max_num = len(first)

    for item in first:
        try:
            pos = reference.index(item['app_label'])
        except ValueError:
            pos = max_num

        ranking.append(pos)

    return [y for x, y in sorted(zip(ranking, first), key=lambda x: x[0])]


def get_admin_url(instance, **kwargs):
    """
    Return the admin URL for the given instance, model class or <app>/<model> string
    """
    url = '#'

    try:

        if type(instance) == str:
            app_label, model_name = instance.split('.')
            url = reverse('admin:{app_label}_{model_name}_changelist'.format(
                app_label=app_label, model_name=model_name
            ))
        elif type(instance) == ModelBase:
            app_label, model_name = instance._meta.app_label, instance._meta.model_name
            url = reverse("admin:{app_label}_{model_name}_changelist".format(
                app_label=app_label, model_name=model_name
            ))
        else:
            app_label, model_name = instance._meta.app_label, instance._meta.model_name
            url = reverse("admin:{app_label}_{model_name}_change".format(
                app_label=app_label, model_name=model_name
            ), args=(instance.pk,))

    except NoReverseMatch:
        logger.error('Couldnt reverse url from {instance}'.format(instance=instance))

    return '{url}?{params}'.format(url=url, params=urlencode(kwargs))


def get_filter_id(spec):
    return getattr(spec, 'field_path', getattr(spec, 'parameter_name', spec.title))


def get_custom_url(url):
    """
    Take in a custom url, and try to reverse it
    """
    if not url:
        logger.warning('No url supplied in custom link')
        return '#'

    if '/' in url:
        return url
    try:
        url = reverse(url)
    except NoReverseMatch:
        logger.warning('Couldnt reverse {url}'.format(url=url))
        url = '#' + url

    return url
