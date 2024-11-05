from importlib.metadata import version as package_version

# We automatically grab the version of `django-jazzmin` from the package manager instead of
# hard coding it.
#
# N.B. For development versions of `django-jazzmin`, the version will be 0.0.0 (see pyproject.toml) as it's
# not technically installed.

version = package_version("django-jazzmin")
__version__ = version
