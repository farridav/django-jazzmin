from django import forms
from django.forms.widgets import Select, SelectMultiple


class AdminlteSelect(Select):

    def _get_media(self):
        return forms.Media(
            css={
                "all": ("admin/plugins/select2/select2.min.css",)
            },
            js=(
                "admin/plugins/select2/select2.min.js",
            ))

    media = property(_get_media)


class AdminlteSelectMultiple(SelectMultiple):
    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs['multiple'] = 'multiple'
        return {**base_attrs, **(extra_attrs or {})}

    def _get_media(self):
        return forms.Media(
            css={
                "all": ("admin/plugins/select2/select2.min.css",)
            },
            js=(
                "admin/plugins/select2/select2.min.js",
            ))

    media = property(_get_media)
