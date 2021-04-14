import logging
from typing import List, Union, Dict, Set, Callable, Any
from urllib.parse import urlencode

from django.apps import apps
from django.contrib.admin import ListFilter
from django.contrib.admin.helpers import AdminForm
from django.contrib.auth.models import AbstractUser
from django.db.models.base import ModelBase, Model
from django.db.models.options import Options
from django.utils.translation import gettext

from jazzmin.compat import NoReverseMatch, reverse

logger = logging.getLogger(__name__)


def order_with_respect_to(original: List, reference: List, getter: Callable = lambda x: x) -> List:
    """
    Order a list based on the location of items in the reference list, optionally, use a getter to pull values out of
    the first list
    """
    ranking = []
    max_num = len(original)
    for item in original:
        try:
            pos = reference.index(getter(item))
        except ValueError:
            pos = max_num

        ranking.append(pos)

    return [y for x, y in sorted(zip(ranking, original), key=lambda x: x[0])]


def get_admin_url(instance: Any, admin_site: str = "admin", from_app: bool = False, **kwargs: str) -> str:
    """
    Return the admin URL for the given instance, model class or <app>.<model> string
    """
    url = "#"

    try:

        if type(instance) == str:
            app_label, model_name = instance.split(".")
            model_name = model_name.lower()
            url = reverse(
                "admin:{app_label}_{model_name}_changelist".format(app_label=app_label, model_name=model_name),
                current_app=admin_site,
            )

        # Model class
        elif instance.__class__ == ModelBase:
            app_label, model_name = instance._meta.app_label, instance._meta.model_name
            url = reverse(
                "admin:{app_label}_{model_name}_changelist".format(app_label=app_label, model_name=model_name),
                current_app=admin_site,
            )

        # Model instance
        elif instance.__class__.__class__ == ModelBase and isinstance(instance, instance.__class__):
            app_label, model_name = instance._meta.app_label, instance._meta.model_name
            url = reverse(
                "admin:{app_label}_{model_name}_change".format(app_label=app_label, model_name=model_name),
                args=(instance.pk,),
                current_app=admin_site,
            )

    except (NoReverseMatch, ValueError):
        # If we are not walking through the models within an app, let the user know this url cant be reversed
        if not from_app:
            logger.warning(gettext("Could not reverse url from {instance}".format(instance=instance)))

    if kwargs:
        url += "?{params}".format(params=urlencode(kwargs))

    return url


def get_filter_id(spec: ListFilter) -> str:
    return getattr(spec, "field_path", getattr(spec, "parameter_name", spec.title))


def get_custom_url(url: str, admin_site: str = "admin") -> str:
    """
    Take in a custom url, and try to reverse it
    """
    if not url:
        logger.warning("No url supplied in custom link")
        return "#"

    if "/" in url:
        return url
    try:
        url = reverse(url.lower(), current_app=admin_site)
    except NoReverseMatch:
        logger.warning("Couldnt reverse {url}".format(url=url))
        url = "#" + url

    return url


def get_model_meta(model_str: str) -> Union[None, Options]:
    """
    Get model meta class
    """
    try:
        app, model = model_str.split(".")
        model_klass: Model = apps.get_registered_model(app, model)
        return model_klass._meta
    except (ValueError, LookupError):
        return None


def get_app_admin_urls(app: str, admin_site: str = "admin") -> List[Dict]:
    """
    For the given app string, get links to all the app models admin views
    """
    if app not in apps.app_configs:
        logger.warning("{app} not found when generating links".format(app=app))
        return []

    models = []
    for model in apps.app_configs[app].get_models():
        url = get_admin_url(model, admin_site=admin_site, from_app=True)

        # We have no admin class
        if url == "#":
            continue

        models.append(
            {
                "url": url,
                "model": "{app}.{model}".format(app=model._meta.app_label, model=model._meta.model_name),
                "name": model._meta.verbose_name_plural.title(),
            }
        )

    return models


def get_view_permissions(user: AbstractUser) -> Set[str]:
    """
    Get model names based on a users view/change permissions
    """
    perms = user.get_all_permissions()
    # the perm codenames should always be lower case
    lower_perms = []
    for perm in perms:
        app, perm_codename = perm.split(".")
        lower_perms.append("{app}.{perm_codename}".format(app=app, perm_codename=perm_codename.lower()))
    return {x.replace("view_", "") for x in lower_perms if "view" in x or "change" in x}


def make_menu(
    user: AbstractUser, links: List[Dict], options: Dict, allow_appmenus: bool = True, admin_site: str = "admin"
) -> List[Dict]:
    """
    Make a menu from a list of user supplied links
    """
    if not user:
        return []

    model_permissions = get_view_permissions(user)

    menu = []
    for link in links:

        perm_matches = []
        for perm in link.get("permissions", []):
            perm_matches.append(user.has_perm(perm))

        if not all(perm_matches):
            continue

        # Url links
        if "url" in link:
            menu.append(
                {
                    "name": link.get("name", "unspecified"),
                    "url": get_custom_url(link["url"], admin_site=admin_site),
                    "children": None,
                    "new_window": link.get("new_window", False),
                    "icon": link.get("icon", options["default_icon_children"]),
                }
            )

        # Model links
        elif "model" in link:
            if link["model"].lower() not in model_permissions:
                continue

            _meta = get_model_meta(link["model"])

            name = _meta.verbose_name_plural.title() if _meta else link["model"]
            menu.append(
                {
                    "name": name,
                    "url": get_admin_url(link["model"], admin_site=admin_site),
                    "children": [],
                    "new_window": link.get("new_window", False),
                    "icon": options["icons"].get(link["model"], options["default_icon_children"]),
                }
            )

        # App links
        elif "app" in link and allow_appmenus:
            children = [
                {"name": child.get("verbose_name", child["name"]), "url": child["url"], "children": None}
                for child in get_app_admin_urls(link["app"], admin_site=admin_site)
                if child["model"] in model_permissions
            ]
            if len(children) == 0:
                continue

            menu.append(
                {
                    "name": getattr(apps.app_configs[link["app"]], "verbose_name", link["app"]).title(),
                    "url": "#",
                    "children": children,
                    "icon": options["icons"].get(link["app"], options["default_icon_children"]),
                }
            )

    return menu


def has_fieldsets_check(adminform: AdminForm) -> bool:
    fieldsets = adminform.fieldsets
    if not fieldsets or (len(fieldsets) == 1 and fieldsets[0][0] is None):
        return False
    return True


def attr(**kwargs) -> Callable:
    def decorator(func: Callable):
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func

    return decorator
