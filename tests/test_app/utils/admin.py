from django.contrib import admin

from .models import AllFields


@admin.register(AllFields)
class AllFieldsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "char",
        "text",
        "slug",
        "email",
        "float",
        "decimal",
        "integer",
        "small_integer",
        "big_integer",
        "positive_integer",
        "boolean",
        "null_boolean",
        "file",
        "file_path",
        "date",
        "date_time",
        "time",
        "duration",
        "identifier",
        "generic_ip_address",
    )
    list_editable = (
        "char",
        "text",
        "slug",
        "email",
        "float",
        "decimal",
        "integer",
        "small_integer",
        "big_integer",
        "positive_integer",
        "boolean",
        "null_boolean",
        "date",
        "date_time",
        "time",
        "duration",
        "identifier",
        "generic_ip_address",
    )
    list_filter = (
        "char",
        "text",
        "slug",
        "email",
        "float",
        "decimal",
        "integer",
        "small_integer",
        "big_integer",
        "positive_integer",
        "boolean",
        "null_boolean",
        "date",
        "date_time",
        "time",
        "duration",
        "identifier",
        "generic_ip_address",
    )
    list_display_links = ("id",)
    fieldsets = (
        ("char", {"fields": ("char", "text", "slug", "email",)}),
        ("number", {"fields": ("float", "decimal", "integer", "small_integer", "big_integer", "positive_integer",)}),
        ("boolean", {"fields": ("boolean", "null_boolean",)}),
        ("file", {"classes": ("collapse",), "fields": ("file", "file_path",)}),
        ("time", {"fields": ("date", "date_time", "time",)}),
        ("other", {"classes": ("collapse",), "fields": ("duration", "identifier", "generic_ip_address",)}),
    )
