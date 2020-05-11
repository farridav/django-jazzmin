import logging

from django.contrib import admin

try:
    from django.urls import reverse, resolve  # NOQA
except ModuleNotFoundError:
    from django.core.urlresolvers import reverse, resolve  # NOQA

logger = logging.getLogger(__name__)


def get_available_apps(request, context):
    # Django 1.9+
    available_apps = context.get('available_apps', [])

    if not available_apps:

        # Django 1.8 on app index only
        available_apps = context.get('app_list')

        # Django 1.8 on rest of the pages
        if not available_apps:
            template_response = admin.site(request.current_app).index(request)
            available_apps = template_response.context_data['app_list']

    if not available_apps:
        logger.warning('Unable to retrieve apps list for menu.')

    return available_apps
