from typing import Any, Dict, Optional

from django import forms
from django.forms.widgets import Select, SelectMultiple


class JazzminSelect(Select):
    template_name = "jazzmin/widgets/select.html"

    @property
    def media(self) -> forms.Media:
        return forms.Media(
            css={"all": ("vendor/select2/css/select2.min.css",)},
            js=("vendor/select2/js/select2.min.js",),
        )


class JazzminSelectMultiple(SelectMultiple):
    template_name = "jazzmin/widgets/select.html"

    def build_attrs(self, base_attrs: Dict[str, Any], extra_attrs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        extra_attrs = extra_attrs or {}
        extra_attrs["multiple"] = "multiple"
        return {**base_attrs, **extra_attrs}

    @property
    def media(self) -> forms.Media:
        return forms.Media(
            css={"all": ("vendor/select2/css/select2.min.css",)},
            js=("vendor/select2/js/select2.min.js",),
        )
