import django

version = "2.6.1"

if django.VERSION < (3, 2):
    default_app_config = "jazzmin.apps.JazzminConfig"
