"""
Regression test for issue #651: Bootswatch CSS files must not reference
missing .map files, or collectstatic fails (e.g. with Whitenoise).

The failure is reproduced when Django's ManifestStaticFilesStorage
post-processes a CSS file that contains sourceMappingURL=bootstrap.min.css.map:
it tries to resolve the referenced file for cache-busting, and raises
ValueError("The file '...bootstrap.min.css.map' could not be found").
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


def test_bootswatch_css_has_no_source_map_reference():
    """
    Bootswatch CSS files must not reference bootstrap.min.css.map.

    Referencing a missing file causes collectstatic to fail when using
    storage backends that validate CSS references (e.g. Whitenoise).
    """
    import jazzmin

    jazzmin_dir = os.path.dirname(jazzmin.__file__)
    bootswatch_dir = os.path.join(jazzmin_dir, "static", "vendor", "bootswatch")
    if not os.path.isdir(bootswatch_dir):
        pytest.skip("Bootswatch static dir not found")

    bad_ref = "sourceMappingURL=bootstrap.min.css.map"
    for name in os.listdir(bootswatch_dir):
        css_path = os.path.join(bootswatch_dir, name, "bootstrap.min.css")
        if not os.path.isfile(css_path):
            continue
        with open(css_path, encoding="utf-8") as f:
            content = f.read()
        assert bad_ref not in content, (
            f"{css_path} contains {bad_ref!r}; remove it so collectstatic does not fail (see #651)"
        )
