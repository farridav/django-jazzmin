"""Tests to ensure Bootstrap 5 migration is complete and no deprecated patterns exist."""

import re
from pathlib import Path

import pytest

import jazzmin


def get_template_files():
    """Get all HTML template files in jazzmin/templates."""
    jazzmin_dir = Path(jazzmin.__file__).parent
    templates_dir = jazzmin_dir / "templates"
    return list(templates_dir.rglob("*.html"))


@pytest.mark.parametrize("template_file", get_template_files(), ids=lambda f: f.name)
def test_no_input_group_append_prepend(template_file):
    """Ensure no templates use deprecated input-group-append or input-group-prepend."""
    content = template_file.read_text()
    deprecated_patterns = ["input-group-append", "input-group-prepend"]

    for pattern in deprecated_patterns:
        assert pattern not in content, (
            f"{template_file.relative_to(template_file.parents[2])} contains deprecated Bootstrap 4 pattern: {pattern}"
        )


@pytest.mark.parametrize("template_file", get_template_files(), ids=lambda f: f.name)
def test_no_btn_block_class(template_file):
    """Ensure no templates use deprecated btn-block class."""
    content = template_file.read_text()
    # Use word boundary to avoid matching btn-block- prefixes
    if re.search(r"\bbtn-block\b", content):
        pytest.fail(
            f"{template_file.relative_to(template_file.parents[2])} contains "
            "deprecated Bootstrap 4 class: btn-block (use w-100 or d-grid instead)"
        )


@pytest.mark.parametrize("template_file", get_template_files(), ids=lambda f: f.name)
def test_no_float_right_left_classes(template_file):
    """Ensure no templates use deprecated float-right or float-left classes."""
    content = template_file.read_text()
    # Allow float-md-right, float-sm-left, etc. (responsive variants)
    # Only catch float-right and float-left without breakpoint suffix
    if re.search(r"\bfloat-(right|left)\b(?!-)", content):
        pytest.fail(
            f"{template_file.relative_to(template_file.parents[2])} contains "
            "deprecated Bootstrap 4 float classes (use float-end/float-start instead)"
        )


@pytest.mark.parametrize("template_file", get_template_files(), ids=lambda f: f.name)
def test_no_old_close_button_pattern(template_file):
    """Ensure no templates use old close button pattern (class='close')."""
    content = template_file.read_text()
    # Match class="close" or class="close something" but not class="btn-close" or class="xxx-close-yyy"
    # Only match when "close" appears as a standalone word at the beginning or middle of class list
    if re.search(r'class=["\'](close\s|.*\sclose\s|.*\sclose["\']|^close["\'])', content):
        pytest.fail(
            f"{template_file.relative_to(template_file.parents[2])} contains "
            "deprecated Bootstrap 4 close button pattern (use btn-close instead)"
        )


@pytest.mark.parametrize("template_file", get_template_files(), ids=lambda f: f.name)
def test_no_data_dismiss_without_bs(template_file):
    """Ensure templates use data-bs-dismiss instead of data-dismiss."""
    content = template_file.read_text()
    # Match data-dismiss but not data-bs-dismiss
    if re.search(r"data-dismiss=(?!.*data-bs-dismiss)", content):
        pytest.fail(
            f"{template_file.relative_to(template_file.parents[2])} contains "
            "deprecated Bootstrap 4 data-dismiss (use data-bs-dismiss instead)"
        )


@pytest.mark.parametrize("template_file", get_template_files(), ids=lambda f: f.name)
def test_no_data_toggle_without_bs(template_file):
    """Ensure templates use data-bs-toggle instead of data-toggle."""
    content = template_file.read_text()
    # Match data-toggle= but not data-bs-toggle=
    # Use word boundary and negative lookahead to avoid matching data-bs-toggle
    # Exclude commented lines
    lines_without_comments = [
        line
        for line in content.split("\n")
        if not line.strip().startswith("{#") and not line.strip().startswith("<!--")
    ]
    content_no_comments = "\n".join(lines_without_comments)

    # Match data-toggle but exclude data-bs-toggle and custom plugin attributes
    if re.search(r"\bdata-toggle=", content_no_comments):
        # Check each occurrence to see if it's deprecated Bootstrap 4
        matches = re.finditer(r"\bdata-toggle=", content_no_comments)
        for match in matches:
            line_start = content_no_comments.rfind("\n", 0, match.start()) + 1
            line_end = content_no_comments.find("\n", match.end())
            if line_end == -1:
                line_end = len(content_no_comments)
            line = content_no_comments[line_start:line_end]

            # Exclude custom plugin attributes (e.g., filer-dropdown from django-filer)
            custom_attrs = ["filer-dropdown", "data-toggle-extra"]
            is_custom = any(attr in line for attr in custom_attrs)

            # If this line uses Bootstrap data-toggle (not custom), it should use data-bs-toggle
            if not is_custom and "data-bs-toggle" not in line:
                pytest.fail(
                    f"{template_file.relative_to(template_file.parents[2])} contains "
                    "deprecated Bootstrap 4 data-toggle (use data-bs-toggle instead)"
                )
                break


def test_login_page_uses_bootstrap5_input_groups():
    """Verify login page uses Bootstrap 5 input group pattern."""
    jazzmin_dir = Path(jazzmin.__file__).parent
    login_template = jazzmin_dir / "templates" / "admin" / "login.html"
    content = login_template.read_text()

    # Should have input-group-text without wrapper divs
    assert "input-group-text" in content, "Login page should use input-group-text"
    assert "input-group-append" not in content, "Login page should not use input-group-append"

    # Should use d-grid for full-width button
    assert "d-grid" in content, "Login page should use d-grid for button layout"


def test_password_reset_uses_bootstrap5_patterns():
    """Verify password reset templates use Bootstrap 5 patterns."""
    jazzmin_dir = Path(jazzmin.__file__).parent
    reset_templates = [
        jazzmin_dir / "templates" / "registration" / "password_reset_form.html",
        jazzmin_dir / "templates" / "registration" / "password_reset_confirm.html",
        jazzmin_dir / "templates" / "registration" / "password_reset_complete.html",
    ]

    for template_path in reset_templates:
        if not template_path.exists():
            continue
        content = template_path.read_text()

        # Should use d-grid for buttons (at least one template)
        if "btn" in content:
            assert "d-grid" in content or "w-100" in content, (
                f"{template_path.name} should use d-grid or w-100 for buttons"
            )


def test_modals_use_bootstrap5_close_button():
    """Verify modals use Bootstrap 5 close button pattern."""
    jazzmin_dir = Path(jazzmin.__file__).parent
    modal_template = jazzmin_dir / "templates" / "jazzmin" / "includes" / "related_modal.html"

    if not modal_template.exists():
        pytest.skip("Modal template not found")

    content = modal_template.read_text()

    # Should use btn-close
    assert "btn-close" in content, "Modal should use btn-close class"
    assert "data-bs-dismiss" in content, "Modal should use data-bs-dismiss"
    # Should NOT have &times; entity
    assert "&times;" not in content, "Modal should not use &times; with btn-close"


def test_main_css_size_reduction():
    """Verify main.css has been significantly reduced in size."""
    jazzmin_dir = Path(jazzmin.__file__).parent
    main_css = jazzmin_dir / "static" / "jazzmin" / "css" / "main.css"

    content = main_css.read_text()
    lines = content.split("\n")

    # Should be under 800 lines (reduced from original 871 lines, with added BS5 compatibility styles)
    assert len(lines) < 800, (
        f"main.css should be under 800 lines (currently {len(lines)} lines). "
        "Keep it lean - only Django-specific fixes and BS5 compatibility."
    )

    # Should contain comments explaining each section
    assert "/*" in content, "main.css should have comments explaining each section"

    # Should contain only Django-specific fixes
    assert "Django" in content or "django" in content, "main.css should be focused on Django-specific fixes"


def test_main_css_no_deprecated_float_patterns():
    """Verify main.css doesn't use deprecated float: right/left."""
    jazzmin_dir = Path(jazzmin.__file__).parent
    main_css = jazzmin_dir / "static" / "jazzmin" / "css" / "main.css"

    content = main_css.read_text()

    # Should not have inline float: right or float: left
    assert not re.search(r"float:\s*(right|left)", content), (
        "main.css should not contain deprecated inline float: right/left patterns"
    )
