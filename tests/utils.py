from collections import defaultdict

from bs4 import BeautifulSoup, Tag
from django.contrib.auth.models import User, Permission
from faker import Faker

fake = Faker()


def user_with_permissions(*permissions):
    """
    Create a user with the given permissions, e.g user_with_permissions('polls.view_poll', 'auth.change_user')
    """
    available_permissions = [
        "{}.{}".format(x[0], x[1]) for x in Permission.objects.values_list("content_type__app_label", "codename")
    ]

    first_name = fake.first_name()
    last_name = fake.last_name()
    user = User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=first_name + "." + last_name + "@fakermail.com",
        username=first_name + last_name,
        password="password",
        is_staff=True,
    )

    for permission in permissions:
        assert permission in available_permissions, "{} not in {}".format(permission, available_permissions)

        app, perm = permission.split(".")
        perm_obj = Permission.objects.get(content_type__app_label=app, codename=perm)
        user.user_permissions.add(perm_obj)

    return user


def parse_sidemenu(response):
    """
    Convert the side menu to a dict keyed on app name, containing a list of links
    """
    menu = defaultdict(list)
    current_app = "Global"
    soup = BeautifulSoup(response.content, "html.parser")

    for li in soup.find(id="jazzy-sidebar").find("ul").find_all("li"):
        if "nav-header" in li["class"]:
            current_app = li.text.strip()

        elif "nav-item" in li["class"]:
            href = li.find("a")["href"]
            menu[current_app].append(href)

    return menu


def parse_topmenu(response):
    """
    Convert the top menu to a list of dicts representing menus, items with submenus will have key 'children'
    """
    menu = []
    soup = BeautifulSoup(response.content, "html.parser")

    for li in soup.find(id="jazzy-navbar").find("ul").find_all("li"):
        anchor = li.find("a")

        # Skip brand link and menu button
        if type(anchor.contents[0]) == Tag:
            continue

        item = {"name": anchor.text.strip(), "link": anchor["href"]}
        dropdown = li.find("div", class_="dropdown-menu")
        if dropdown:
            item["children"] = [{"name": a.text.strip(), "link": a["href"]} for a in dropdown.find_all("a")]

        menu.append(item)

    return menu


def parse_usermenu(response):
    """
    Convert the user menu to a list of dicts representing menus
    """
    menu = []
    soup = BeautifulSoup(response.content, "html.parser")

    for link in soup.find(id="jazzy-usermenu").find_all("a"):
        item = {"name": link.text.strip(), "link": link["href"]}
        menu.append(item)

    return menu
