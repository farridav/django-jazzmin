from django.contrib import admin

from .models import BookLoan


class BookLoanInline(admin.StackedInline):
    model = BookLoan
    extra = 1
    readonly_fields = ("id",)
    fields = ("book", "imprint", "status", "due_back", "borrower", "duration")


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
