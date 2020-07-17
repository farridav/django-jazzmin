import copy
import itertools
import json
import logging
import urllib.parse

from django.conf import settings
from django.contrib.admin.helpers import AdminForm
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views.main import PAGE_VAR
from django.contrib.auth import get_user_model
from django.contrib.auth.context_processors import PermWrapper
from django.http import HttpRequest
from django.template import Library
from django.template.loader import get_template
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import get_text_list
from django.utils.translation import gettext

from .. import version
from ..settings import get_settings, get_ui_tweaks, CHANGEFORM_TEMPLATES
from ..utils import (
    order_with_respect_to,
    get_filter_id,
    get_admin_url,
    get_view_permissions,
    make_menu,
)

User = get_user_model()
register = Library()
logger = logging.getLogger(__name__)


@register.simple_tag(takes_context=True)
def get_side_menu(context):
    """
    Get the list of apps and models to render out in the side menu and on the dashboard page
    """

    user = context.get("user")
    if not user:
        return []

    model_permissions = get_view_permissions(user)
    options = get_settings()

    menu = []
    available_apps = copy.deepcopy(context.get("available_apps", []))
    custom_links = {
        app_name: make_menu(user, links, options, allow_appmenus=False)
        for app_name, links in options.get("custom_links", {}).items()
    }

    for app in available_apps:
        app_label = app["app_label"].lower()
        app["icon"] = options["icons"].get(app_label, options["default_icon_parents"])
        if app_label in options["hide_apps"]:
            continue

        menu_items = []
        for model in app.get("models", []):
            model_str = "{app_label}.{model}".format(app_label=app_label, model=model["object_name"]).lower()
            if model_str not in model_permissions:
                continue
            if model_str in options.get("hide_models", []):
                continue

            model["url"] = model["admin_url"]
            model["icon"] = options["icons"].get(model_str, options["default_icon_children"])
            menu_items.append(model)

        menu_items.extend(custom_links.get(app_label, []))

        if len(menu_items):
            app["models"] = menu_items
            menu.append(app)

    if options.get("order_with_respect_to"):
        menu = order_with_respect_to(menu, options["order_with_respect_to"])

    return menu


@register.simple_tag
def get_top_menu(user):
    """
    Produce the menu for the top nav bar
    """
    options = get_settings()
    return make_menu(user, options.get("topmenu_links", []), options, allow_appmenus=True)


@register.simple_tag
def get_user_menu(user):
    """
    Produce the menu for the user dropdown
    """
    options = get_settings()
    return make_menu(user, options.get("usermenu_links", []), options, allow_appmenus=False)


@register.simple_tag
def get_jazzmin_settings():
    """
    Return Jazzmin settings
    """
    return get_settings()


@register.simple_tag
def get_jazzmin_ui_tweaks():
    """
    Return Jazzmin ui tweaks
    """
    return get_ui_tweaks()


@register.simple_tag
def get_jazzmin_version():
    """
    Get the version for this package
    """
    return version


@register.simple_tag
def get_user_avatar(user):
    """
    For the given user, try to get the avatar image
    """
    no_avatar = static("adminlte/img/user2-160x160.jpg")
    options = get_settings()

    if not options.get("user_avatar"):
        return no_avatar

    avatar_field = getattr(user, options["user_avatar"], None)
    if avatar_field:
        return avatar_field.url

    return no_avatar


@register.simple_tag
def jazzmin_paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == ".":
        html_str = """
            <li class="page-item">
            <a class="page-link" href="javascript:void(0);" data-dt-idx="3" tabindex="0">… </a>
            </li>
        """

    elif i == cl.page_num:
        html_str = """
            <li class="page-item active">
            <a class="page-link" href="javascript:void(0);" data-dt-idx="3" tabindex="0">{num}
            </a>
            </li>
        """.format(
            num=i + 1
        )

    else:
        query_string = cl.get_query_string({PAGE_VAR: i})
        end = mark_safe("end" if i == cl.paginator.num_pages - 1 else "")
        html_str = """
            <li class="page-item">
            <a href="{query_string}" class="page-link {end}" data-dt-idx="3" tabindex="0">{num}</a>
            </li>
        """.format(
            num=i + 1, query_string=query_string, end=end
        )

    return format_html(html_str)


@register.simple_tag
def admin_extra_filters(cl):
    """
    Return the dict of used filters which is not included in list_filters form
    """
    used_parameters = list(itertools.chain(*(s.used_parameters.keys() for s in cl.filter_specs)))
    return dict((k, v) for k, v in cl.params.items() if k not in used_parameters)


@register.simple_tag
def jazzmin_list_filter(cl, spec):
    tpl = get_template(spec.template)
    choices = list(spec.choices(cl))
    field_key = get_filter_id(spec)
    matched_key = field_key
    for choice in choices:
        query_string = choice["query_string"][1:]
        query_parts = urllib.parse.parse_qs(query_string)

        value = ""
        matches = {}
        for key in query_parts.keys():
            if key == field_key:
                value = query_parts[key][0]
                matched_key = key
            elif key.startswith(field_key + "__") or "__" + field_key + "__" in key:
                value = query_parts[key][0]
                matched_key = key

            if value:
                matches[matched_key] = value

        # Iterate matches, use first as actual values, additional for hidden
        i = 0
        for key, value in matches.items():
            if i == 0:
                choice["name"] = key
                choice["value"] = value
            i += 1

    return tpl.render({"field_name": field_key, "title": spec.title, "choices": choices, "spec": spec,})


@register.filter
def jazzy_admin_url(value):
    """
    Get the admin url for a given object
    """
    return get_admin_url(value)


@register.filter
def has_fieldsets(value):
    """
    Do we have fieldsets
    """
    fieldsets = value.model_admin.fieldsets
    has_fieldsets = fieldsets and len(fieldsets) > 1
    return True if has_fieldsets else False


@register.filter
def debug(value):
    """
    Add in a breakpoint here and use filter in templates for debugging ;)
    """
    return type(value)


@register.filter
def as_json(value):
    """
    Take the given item and dump it out as JSON
    """
    return json.dumps(value)


@register.simple_tag
def get_changeform_template(adminform: AdminForm) -> str:
    """
    Go get the correct change form template based on the modeladmin being used,
    the default template, or the overriden one for this modeladmin
    """
    options = get_settings()
    fieldsets = adminform.model_admin.fieldsets
    has_fieldsets = fieldsets and len(fieldsets) > 1
    inlines = adminform.model_admin.inlines
    has_inlines = inlines and len(inlines) > 0
    model = adminform.model_admin.model
    model_name = "{}.{}".format(model._meta.app_label, model._meta.model_name).lower()

    format = options.get("changeform_format", "")
    if model_name in options.get("changeform_format_overrides", {}):
        format = options["changeform_format_overrides"][model_name]

    if not has_fieldsets and not has_inlines:
        return CHANGEFORM_TEMPLATES.get("single")

    if not format or format not in CHANGEFORM_TEMPLATES.keys():
        return CHANGEFORM_TEMPLATES.get("horizontal_tabs")

    return CHANGEFORM_TEMPLATES.get(format)


@register.simple_tag
def sidebar_status(request: HttpRequest) -> str:
    """
    Check if our sidebar is open or closed
    """
    if request.COOKIES.get("jazzy_menu", "") == "closed":
        return "sidebar-collapse"
    return ""


@register.filter
def can_view_self(perms: PermWrapper) -> bool:
    """
    Determines whether a user has sufficient permissions to view its own profile
    """
    view_perm = "{}.view_{}".format(User._meta.app_label, User._meta.model_name)

    return perms[User._meta.app_label][view_perm]


@register.simple_tag
def header_class(header: dict, forloop: dict) -> str:
    """
    Adds CSS classes to header HTML element depending on its attributes
    """
    classes = []
    sorted, asc, desc = (
        header.get("sorted"),
        header.get("ascending"),
        header.get("descending"),
    )

    if forloop["counter0"] == 0:
        classes.append("djn-checkbox-select-all")

    if not header["sortable"]:
        return " ".join(classes)

    if sorted and asc:
        classes.append("sorting_asc")
    elif sorted and desc:
        classes.append("sorting_desc")
    else:
        classes.append("sorting")

    return " ".join(classes)


@register.filter
def app_is_installed(app: str) -> bool:
    """
    Checks if an app has been installed under INSTALLED_APPS on the project settings
    """
    return app in settings.INSTALLED_APPS


@register.simple_tag
def action_message_to_list(action: LogEntry) -> list:
    """
    Retrieves a formatted list with all actions taken by a user given a log entry object
    """
    messages = []
    if action.change_message and action.change_message[0] == "[":
        try:
            change_message = json.loads(action.change_message)
        except json.JSONDecodeError:
            return [action.change_message]

        for sub_message in change_message:
            if "added" in sub_message:
                if sub_message["added"]:
                    sub_message["added"]["name"] = gettext(sub_message["added"]["name"])
                    messages.append(gettext("Added {name} “{object}”.").format(**sub_message["added"]))
                else:
                    messages.append(gettext("Added."))

            elif "changed" in sub_message:
                sub_message["changed"]["fields"] = get_text_list(
                    [gettext(field_name) for field_name in sub_message["changed"]["fields"]], gettext("and"),
                )
                if "name" in sub_message["changed"]:
                    sub_message["changed"]["name"] = gettext(sub_message["changed"]["name"])
                    messages.append(gettext("Changed {fields} for {name} “{object}”.").format(**sub_message["changed"]))
                else:
                    messages.append(gettext("Changed {fields}.").format(**sub_message["changed"]))

            elif "deleted" in sub_message:
                sub_message["deleted"]["name"] = gettext(sub_message["deleted"]["name"])
                messages.append(gettext("Deleted {name} “{object}”.").format(**sub_message["deleted"]))
    return messages if len(messages) else [action.change_message]


@register.filter
def get_action_icon(message: str) -> str:
    """
    Retrieves action given a certain action
    """
    if message.startswith("Added"):
        return "plus-circle"
    elif message.startswith("Deleted"):
        return "trash"
    else:
        return "edit"


@register.filter
def get_action_color(message: str) -> str:
    """
    Retrieves color given a certain action
    """
    if message.startswith("Added"):
        return "success"
    elif message.startswith("Deleted"):
        return "danger"
    else:
        return "blue"


@register.filter
def style_bold_first_word(message: str) -> str:
    """
    Wraps first word in a message with <strong> HTML element
    """
    message_words = message.split()

    if not len(message_words):
        return ""

    message_words[0] = "<strong>{}</strong>".format(message_words[0])

    message = " ".join([word for word in message_words])

    return format_html(message)
