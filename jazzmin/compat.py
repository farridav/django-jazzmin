"""
Compatibility shims for Django URL resolution across versions.
"""

try:
    from django.urls import NoReverseMatch, resolve, reverse
except ImportError:
    from django.core.urlresolvers import NoReverseMatch, resolve, reverse

__all__ = ["NoReverseMatch", "resolve", "reverse"]
