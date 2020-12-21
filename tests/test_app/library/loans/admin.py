from django.contrib import admin
from django.urls import path

from .models import BookLoan, Library
from .views import CustomView


class BookLoanInline(admin.StackedInline):
    model = BookLoan
    extra = 1
    readonly_fields = ("id", "duration")
    fields = (
        "book",
        "imprint",
        "status",
        "due_back",
        "borrower",
        "loan_start",
        "duration",
    )


@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "borrower", "due_back", "id")
    list_filter = ("status", "due_back")
    autocomplete_fields = ("borrower",)
    search_fields = ("book__title",)
    readonly_fields = ("id",)
    fieldsets = (
        (None, {"fields": ("book", "imprint", "id")}),
        ("Availability", {"fields": ("status", "due_back", "duration", "borrower")}),
    )

    def get_urls(self):
        """
        Add in a custom view to demonstrate =
        """
        urls = super().get_urls()
        return urls + [path("custom_view", CustomView.as_view(), name="custom_view")]

    def response_change(self, request, obj):
        ret = super().response_change(request, obj)

        if "reserve" in request.POST:
            obj.status = "r"
            obj.save()
        return ret


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "librarian")
