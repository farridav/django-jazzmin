#!/usr/bin/env python

import argparse
import os
import subprocess
from itertools import chain

import django
import polib

THIS_DIR = os.path.dirname(__file__)
LOCALE_DIR = os.path.join(THIS_DIR, "jazzmin", "locale")
DJANGO_PATH = django.__path__[0]


def locales(cmd_args: argparse.Namespace):
    """
    e.g - ./cli.py locales --prune de
    """
    our_po = polib.pofile(os.path.join(LOCALE_DIR, cmd_args.locale, "LC_MESSAGES", "django.po"))
    admin_po = polib.pofile(os.path.join(DJANGO_PATH, "contrib", "admin", "locale", "en", "LC_MESSAGES", "django.po"))
    admindocs_po = polib.pofile(
        os.path.join(
            DJANGO_PATH,
            "contrib",
            "admindocs",
            "locale",
            "en",
            "LC_MESSAGES",
            "django.po",
        )
    )
    existing_strings = {x.msgid for x in chain(admin_po, admindocs_po)}
    new_po = polib.POFile()
    new_po.metadata = our_po.metadata
    for po in our_po:
        if po.msgid not in existing_strings:
            new_po.append(po)

    new_po.save(os.path.join(LOCALE_DIR, cmd_args.locale, "LC_MESSAGES", "django.po"))


def templates(cmd_args: argparse.Namespace):
    """
    Generate diffs/patch files for all the templates we override, useful for seeing whats changed

    ./cli.py templates --diff

    """
    diffs = os.path.join(THIS_DIR, "diffs")
    templates = {
        os.path.join(THIS_DIR, "jazzmin", "templates", "admin"): os.path.join(
            DJANGO_PATH, "contrib", "admin", "templates", "admin"
        ),
        os.path.join(THIS_DIR, "jazzmin", "templates", "admin_doc"): os.path.join(
            DJANGO_PATH, "contrib", "admindocs", "templates", "admin_doc"
        ),
    }

    for jazzmin_dir, django_dir in templates.items():
        for template in [os.path.join(dp, f) for dp, dn, filenames in os.walk(jazzmin_dir) for f in filenames]:
            original = template.replace(jazzmin_dir, django_dir)
            if os.path.isfile(original):
                result = subprocess.run(
                    ["diff", "-u", "-w", "--suppress-common-lines", original, template],
                    stdout=subprocess.PIPE,
                )
                out_file = template.replace(jazzmin_dir, diffs) + ".patch"
                os.makedirs(os.path.dirname(out_file), exist_ok=True)

                with open(out_file, "wb+") as fp:
                    fp.write(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True

    parser_locales = subparsers.add_parser("locales", help="remove the django provided strings")
    parser_locales.add_argument("--prune", action="store", dest="locale", help="locale to prune", default="de")
    parser_locales.set_defaults(func=locales)

    parser_templates = subparsers.add_parser("templates", help="Deal with templates")
    parser_templates.add_argument(
        "--diff",
        action="store_true",
        dest="template_diff",
        help="generate template diff",
    )
    parser_templates.set_defaults(func=templates)

    try:
        cmd_args = parser.parse_args()
    except TypeError:
        parser.print_help()
        return

    cmd_args.func(cmd_args)


if __name__ == "__main__":
    main()
