import sys

# We automatically grab the version of `django-jazzmin` from the package manager instead of
# hard coding it. The method for determining the version changed since PY3.8. N.B. For
# development versions of `django-jazzmin`, the version will be 0.0.0 (see pyproject.toml) as it's
# not technically installed.
if sys.version_info >= (3, 8):
    from importlib.metadata import version as package_version

    version = package_version("django-jazzmin")
else:
    import pkg_resources

    version = pkg_resources.get_distribution("django-jazzmin").version
