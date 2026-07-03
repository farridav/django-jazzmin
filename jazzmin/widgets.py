from typing import Any
from django.forms.widgets import Select, SelectMultiple


class JazzminSelect(Select):
    template_name = "jazzmin/widgets/select.html"

    def build_attrs(self, base_attrs: dict[str, Any], extra_attrs: dict[str, Any] | None = None) -> dict[str, Any]:
        attrs = super().build_attrs(base_attrs, extra_attrs)
        classes = attrs.get("class", "")
        if "form-select" not in classes:
            attrs["class"] = f"{classes} form-select".strip()
        return attrs


class JazzminSelectMultiple(SelectMultiple):
    template_name = "jazzmin/widgets/select.html"

    def build_attrs(self, base_attrs: dict[str, Any], extra_attrs: dict[str, Any] | None = None) -> dict[str, Any]:
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["multiple"] = "multiple"
        classes = attrs.get("class", "")
        if "form-control" not in classes:
            attrs["class"] = f"{classes} form-control".strip()
        return attrs