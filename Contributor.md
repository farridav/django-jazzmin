# Navbar still in light mode even DarkMode is applied #515

 ret = {
        "raw": raw_tweaks,
        "theme": {"name": theme, "src": static(THEMES[theme])},
        "sidebar_classes": classes("sidebar", "sidebar_disable_expand"),
        "navbar_classes": classes("no_navbar_border", "navbar_small_text"),
        "body_classes": classes(
            "accent", "body_small_text", "navbar_fixed", "footer_fixed", "sidebar_fixed", "layout_boxed"
        )
        + theme_body_classes,
        "actions_classes": classes("actions_sticky_top"),
        "sidebar_list_classes": classes(
            "sidebar_nav_small_text",
            "sidebar_nav_flat_style",
            "sidebar_nav_legacy_style",
            "sidebar_nav_child_indent",
            "sidebar_nav_compact_style",
        ),
        "brand_classes": classes("brand_small_text", "brand_colour"),
        "footer_classes": classes("footer_small_text"),
        "button_classes": tweaks["button_classes"],
    }

default  "navbar": "navbar-white navbar-light", was also added to the "navbar_classes" which was overwriting dark navbar classes
