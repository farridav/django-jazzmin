from django import forms
from django.forms.widgets import Select, SelectMultiple


class JazzminSelect(Select):
    template_name = "jazzmin/widgets/select.html"

    @property
    def media(self):
        return forms.Media(
            css={"all": ("adminlte/plugins/select2/select2.min.css",)}, js=("adminlte/plugins/select2/select2.min.js",)
        )


class JazzminSelectMultiple(SelectMultiple):
    template_name = "jazzmin/widgets/select.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs["multiple"] = "multiple"
        return {**base_attrs, **(extra_attrs or {})}

    @property
    def media(self):
        return forms.Media(
            css={"all": ("adminlte/plugins/select2/select2.min.css",)}, js=("adminlte/plugins/select2/select2.min.js",)
        )
