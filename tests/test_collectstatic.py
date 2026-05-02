"""
Regression test for issue #651: Bootswatch CSS files reference
sourceMappingURL=bootstrap.min.css.map; the .map files must be present
or collectstatic fails (e.g. with Whitenoise).
"""

import os

import pytest
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.management import call_command
from django.test import override_settings


def test_manifest_storage_fails_when_css_references_missing_source_map(tmp_path):
    """
    Reproduce #651: post-processing a CSS file that references a missing
    .map file yields ValueError.

    ManifestStaticFilesStorage rewrites sourceMappingURL in CSS to hashed
    filenames; resolving the target requires the file to exist. If the
    .map file is not shipped, resolution fails.
    """
    from django.core.files.storage import FileSystemStorage

    # Create a CSS file that references a missing .map (as Bootswatch themes did)
    css_dir = tmp_path / "vendor" / "bootswatch" / "test"
    css_dir.mkdir(parents=True)
    (css_dir / "bootstrap.min.css").write_text("/*! theme */\n/*# sourceMappingURL=bootstrap.min.css.map */\n")
    css_path = "vendor/bootswatch/test/bootstrap.min.css"
    source_storage = FileSystemStorage(location=str(tmp_path))
    paths = {css_path: (source_storage, css_path)}

    with override_settings(STATIC_ROOT=str(tmp_path)):
        dest_storage = ManifestStaticFilesStorage()
        processor = dest_storage.post_process(paths, dry_run=False)
        results = list(processor)
    errors = [r for r in results if isinstance(r[2], ValueError)]
    assert errors, "Expected ValueError when CSS references missing .map file"
    assert "bootstrap.min.css.map" in str(errors[0][2])


@pytest.mark.django_db
def test_collectstatic_succeeds_with_manifest_storage(tmp_path):
    """
    collectstatic must succeed with ManifestStaticFilesStorage.

    Bootswatch bootstrap.min.css files used to contain
    sourceMappingURL=bootstrap.min.css.map while the .map files were not
    shipped, causing Whitenoise/Django to fail during collectstatic.
    """
    with override_settings(STATIC_ROOT=str(tmp_path)):
        call_command("collectstatic", "--noinput", verbosity=0)


def test_bootswatch_css_map_files_exist_when_referenced():
    """
    When a Bootswatch CSS references bootstrap.min.css.map, the .map file
    must exist in the same directory so collectstatic succeeds (see #651).
    """
    import jazzmin

    jazzmin_dir = os.path.dirname(jazzmin.__file__)
    bootswatch_dir = os.path.join(jazzmin_dir, "static", "vendor", "bootswatch")
    if not os.path.isdir(bootswatch_dir):
        pytest.skip("Bootswatch static dir not found")

    ref = "sourceMappingURL=bootstrap.min.css.map"
    for name in os.listdir(bootswatch_dir):
        theme_dir = os.path.join(bootswatch_dir, name)
        css_path = os.path.join(theme_dir, "bootstrap.min.css")
        map_path = os.path.join(theme_dir, "bootstrap.min.css.map")
        if not os.path.isfile(css_path):
            continue
        with open(css_path, encoding="utf-8") as f:
            content = f.read()
        if ref in content and not os.path.isfile(map_path):
            pytest.fail(f"{css_path} references bootstrap.min.css.map but {map_path} is missing (see #651)")
