from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.timesince import timesince
from jazzmin.utils import attr

from ..loans.admin import BookLoanInline
from .models import Author, Book, Genre

admin.site.unregister(User)


class BooksInline(admin.TabularInline):
    model = Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ("general", {"fields": ("title", "author", "library"), "description": "General book fields"}),
        ("other", {"fields": ("genre", "summary", "isbn", "published_on", "pages")}),
    )
    raw_id_fields = ("author",)
    list_display = ("__str__", "title", "author", "pages")
    readonly_fields = ("__str__",)
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ("title",)
    search_fields = ("title", "author__last_name")
    autocomplete_fields = ("genre",)
    date_hierarchy = "published_on"
    save_as = True
    save_on_top = True
    inlines = (BookLoanInline,)

    actions_on_bottom = True

    # Order the sections within the change form
    jazzmin_section_order = ("book loans", "general", "other")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")
    fields = ("first_name", "last_name", ("date_of_birth", "date_of_death"))
    inlines = (BooksInline,)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "object", "action_flag", "change_message", "modified")
    readonly_fields = ["object", "modified"]
    search_fields = ("user__email",)
    date_hierarchy = "action_time"
    list_filter = ("action_flag", "content_type__model")
    list_per_page = 20

    def object(self, obj):
        url = obj.get_admin_url()
        return format_html(
            '<a href="{url}">{obj} [{model}]</a>'.format(url=url, obj=obj.object_repr, model=obj.content_type.model)
        )

    @attr(admin_order_field="action_time")
    def modified(self, obj):
        if not obj.action_time:
            return "Never"
        return "{} ago".format(timesince(obj.action_time))


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        """
        Remove our test user from the admin, so it cant be messed with
        """
        return super(CustomUserAdmin, self).get_queryset(request).exclude(username="test@test.com")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)
