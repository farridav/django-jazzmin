from django import forms
from django.forms.widgets import Select, SelectMultiple


class AdminlteSelect(Select):
    template_name = "adminlte/widgets/select.html"

    @property
    def media(self):
        return forms.Media(
            css={"all": ("admin/plugins/select2/select2.min.css",)}, js=("admin/plugins/select2/select2.min.js",)
        )


class AdminlteSelectMultiple(SelectMultiple):
    template_name = "adminlte/widgets/select.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs['multiple'] = 'multiple'
        return {**base_attrs, **(extra_attrs or {})}

    @property
    def media(self):
        return forms.Media(
            css={"all": ("admin/plugins/select2/select2.min.css",)}, js=("admin/plugins/select2/select2.min.js",)
        )
