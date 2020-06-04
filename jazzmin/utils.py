import logging
from urllib.parse import urlencode

from django.apps import apps
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
            app_label, model_name = instance.lower().split('.')
            url = reverse('admin:{app_label}_{model_name}_changelist'.format(
                app_label=app_label, model_name=model_name
            ))

        # Model class
        elif instance.__class__ == ModelBase:
            app_label, model_name = instance._meta.app_label, instance._meta.model_name
            url = reverse("admin:{app_label}_{model_name}_changelist".format(
                app_label=app_label, model_name=model_name
            ))

        # Model instance
        elif instance.__class__.__class__ == ModelBase and isinstance(instance, instance.__class__):
            app_label, model_name = instance._meta.app_label, instance._meta.model_name
            url = reverse("admin:{app_label}_{model_name}_change".format(
                app_label=app_label, model_name=model_name
            ), args=(instance.pk,))

    except NoReverseMatch:
        logger.error('Couldnt reverse url from {instance}'.format(instance=instance))

    if kwargs:
        url += '?{params}'.format(params=urlencode(kwargs))

    return url


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


def get_model_meta(model_str):
    """
    Get the plural name
    """
    app, model = model_str.split('.')
    Model = apps.get_registered_model(app, model)
    return Model._meta


def get_app_admin_urls(app):
    """
    For the given app string, get links to all the app models admin views
    """
    if app not in apps.app_configs:
        logger.warning('{app} not found when generating links'.format(app=app))
        return []

    models = []
    for model in apps.app_configs[app].get_models():
        url = get_admin_url(model)

        # We have no admin class
        if url == '#':
            continue

        models.append({
            'url': get_admin_url(model),
            'model': '{app}.{model}'.format(app=model._meta.app_label, model=model._meta.model_name),
            'name': model._meta.verbose_name_plural.title()
        })

    return models


def get_model_permissions(user):
    """
    Create model permissions from the users permissions,

    e.g having any of auth.view_user, auth.change_user, auth.delete_user will grant you auth.user
    """
    permissions = set()
    for permission in user.get_all_permissions():
        app_label, model = permission.split('.')
        model = model.split('_')[1]
        permissions.add('{app_label}.{model}'.format(app_label=app_label, model=model))

    return permissions
