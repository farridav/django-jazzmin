from django.apps import apps
from django.contrib.staticfiles import finders
from django.urls import NoReverseMatch, reverse


def validate_app_or_model(value: str) -> str:
    """
    Validate either an app or a model
    """
    if "." not in value:
        return validate_app(value)

    return validate_model(value)


def validate_app(value: str) -> str:
    """
    Validate app name
    """
    app_names = apps.app_configs.keys()
    if value not in app_names:
        raise ValueError(f"App '{value}' not one of {', '.join(app_names)}")

    return value


def validate_model(value: str) -> str:
    """
    Validate model name in the format 'app.model'
    """
    if "." not in value:
        raise ValueError(f"Search model '{value}' is not in the format 'app.model'")

    app, model = value.split(".")
    validate_app(app)

    models = apps.all_models[app].keys()
    if model not in models:
        raise ValueError(f"Model '{model}' not one of {', '.join(models)}")

    return value


def validate_static_file(value: str) -> str:
    """
    find the file using djangos static file finder
    """
    if not finders.find(value):
        raise ValueError(f"Static file '{value}' not found")
    return value


def validate_link(value: str) -> str:
    """
    Validate a link
    """
    value = value.lower().strip()

    if ":" in value:
        try:
            value = reverse(value, current_app=admin_site)
        except NoReverseMatch:
            logger.warning(f"Couldnt reverse {value}")
            value = "#" + value

    if not value:
        raise ValueError("Link is empty")

    return value
