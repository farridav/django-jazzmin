import logging

from django.contrib.admin import AdminSite

try:
    from django.urls import reverse, resolve  # NOQA
except ModuleNotFoundError:
    from django.core.urlresolvers import reverse, resolve  # NOQA

logger = logging.getLogger(__name__)


def get_admin_site(current_app):
    """
    Method tries to get actual admin.site class, if any custom admin sites
    were used. Couldn't find any other references to actual class other than
    in func_closer dict in index() func returned by resolver.
    """
    try:
        resolver_match = resolve(reverse('%s:index' % current_app))
        # Django 1.9 exposes AdminSite instance directly on view function
        if hasattr(resolver_match.func, 'admin_site'):
            return resolver_match.func.admin_site

        for func_closure in resolver_match.func.__closure__:
            if isinstance(func_closure.cell_contents, AdminSite):
                return func_closure.cell_contents
    except Exception as e:
        logger.exception(e, 'TODO: catch this instead')
        pass

    from django.contrib import admin
    return admin.site


def get_available_apps(request, context):
    # Django 1.9+
    available_apps = context.get('available_apps', [])

    if not available_apps:

        # Django 1.8 on app index only
        available_apps = context.get('app_list')

        # Django 1.8 on rest of the pages
        if not available_apps:
            try:
                template_response = get_admin_site(request.current_app).index(request)
                available_apps = template_response.context_data['app_list']
            except Exception as e:
                logger.exception(e, 'TODO: catch this instead')
                pass

    if not available_apps:
        logger.warning('adminlteui was unable to retrieve apps list for menu.')

    return available_apps
