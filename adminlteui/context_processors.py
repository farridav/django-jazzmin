from django.conf import settings


def adminlte_settings(request):
    if hasattr(settings, 'ADMINLTE_SETTINGS'):
        return {
            'adminlte': settings.ADMINLTE_SETTINGS
        }
    else:
        return {
            'adminlte': {}
        }
