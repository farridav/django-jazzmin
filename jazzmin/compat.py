try:
    from django.urls import reverse, resolve, NoReverseMatch  # NOQA
except ImportError:
    from django.core.urlresolvers import reverse, resolve, NoReverseMatch  # NOQA
