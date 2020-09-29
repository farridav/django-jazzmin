#!/usr/bin/env python

import argparse
import os
from itertools import chain

import django
import polib

THIS_DIR = os.path.dirname(__file__)
LOCALE_DIR = os.path.join(THIS_DIR, "jazzmin", "locale")


def locales(cmd_args):
    """
    1. cd into the jazzmin folder
    2. Add the desired language directory e.g mkdir -p locale/de/LC_MESSAGES
    3. Run django-admin makemessages
    4. Run ./cli.py locales --locale de to remove the django provided strings
    5. Go through the strings in the locale file, any that are not genuinely new strings introduced by jazzmin, find
    them in the codebase, and try making them match the ones provided in either of djangos translation files

    https://raw.githubusercontent.com/django/django/master/django/contrib/admindocs/locale/de/LC_MESSAGES/django.po
    https://raw.githubusercontent.com/django/django/master/django/contrib/admin/locale/de/LC_MESSAGES/django.po

    Once you have finished, run makemessages again, until the file contains ONLY unique strings to jazzmin, there should
    only be a handful
    """
    django_path = django.__path__[0]
    our_po = polib.pofile(os.path.join(LOCALE_DIR, cmd_args.locale, "LC_MESSAGES", "django.po"))
    admin_po = polib.pofile(os.path.join(django_path, "contrib", "admin", "locale", "en", "LC_MESSAGES", "django.po"))
    admindocs_po = polib.pofile(
        os.path.join(django_path, "contrib", "admindocs", "locale", "en", "LC_MESSAGES", "django.po")
    )
    existing_strings = {x.msgid for x in chain(admin_po, admindocs_po)}
    new_po = polib.POFile()
    new_po.metadata = our_po.metadata
    for po in our_po:
        if po.msgid not in existing_strings:
            new_po.append(po)

    new_po.save(os.path.join(LOCALE_DIR, cmd_args.locale, "LC_MESSAGES", "django.po"))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_locales = subparsers.add_parser('locales', help='remove the django provided strings')
    parser_locales.add_argument("--locale", action="store", dest="locale", help="locale to process", default="de")
    parser_locales.set_defaults(func=locales)
    cmd_args = parser.parse_args()
    cmd_args.func(cmd_args)


if __name__ == "__main__":
    main()
