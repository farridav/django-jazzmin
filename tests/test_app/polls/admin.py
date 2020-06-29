from collections import defaultdict

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.utils.timesince import timesince

from tests.test_app.polls.models import Campaign, Cheese, AllFields
from .models import Poll, Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    show_change_link = True


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    fieldsets = (
        ("general", {"fields": ("owner",)}),
        ("other", {"fields": ("text", "pub_date", "active")}),
    )
    raw_id_fields = ("owner",)
    list_display = ("owner", "text", "pub_date", "active")
    list_display_links = ()
    list_filter = ("active", "owner")
    list_select_related = False
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ("active",)
    search_fields = ("text", "owner__email")
    date_hierarchy = "pub_date"
    save_as = True
    save_as_continue = True
    save_on_top = True
    preserve_filters = True
    inlines = (ChoiceInline,)

    actions = []
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("poll", "choice_text")
    list_per_page = 20
    list_editable = ("choice_text",)
    autocomplete_fields = ("poll",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "poll", "choice")


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "object",
        "action_flag",
        "change_message",
        "modified",
    )
    readonly_fields = ["object", "modified"]
    search_fields = ("user__email",)
    date_hierarchy = "action_time"
    list_filter = ("action_flag", "content_type__model")
    list_per_page = 20

    def object(self, obj):
        url = obj.get_admin_url()
        return format_html(
            '<a href="{url}">{obj} [{model}]</a>'.format(
                url=url, obj=obj.object_repr, model=obj.content_type.model
            )
        )

    def modified(self, obj):
        if not obj.action_time:
            return "Never"
        return "{} ago".format(timesince(obj.action_time))

    modified.admin_order_field = "action_time"


@admin.register(Cheese)
class CheeseAdmin(admin.ModelAdmin):
    list_display = ("name", "stinky")
    is_editable = ("name", "stinky")


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("id", "promoter")
    search_fields = ("promoter__email", "promoter__username")
    autocomplete_fields = (
        "polls",
        "promoter",
    )


@admin.register(AllFields)
class AllFieldsAdmin(admin.ModelAdmin):
    filter_vertical = ("many_to_many_vertical",)
    autocomplete_fields = ("foreign_key_autocomplete",)
    raw_id_fields = ("foreign_key_by_id",)
    list_display_links = ("id",)

    @property
    def all_fields(self):
        fields = [field.name for field in AllFields._meta.fields]
        many_to_many = [field.name for field in AllFields._meta.many_to_many]
        return list(self.readonly_fields) + fields + many_to_many

    @property
    def list_display(self):
        fields = self.all_fields
        fields.remove('many_to_many')
        fields.remove('many_to_many_vertical')
        return fields

    @property
    def list_editable(self):
        fields = self.all_fields
        fields.remove('id')
        fields.remove('many_to_many')
        fields.remove('many_to_many_vertical')
        return fields

    def get_list_filter(self, request):
        return self.all_fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = defaultdict(list)
        disallowed = ['id']
        fields = AllFields._meta.fields + AllFields._meta.many_to_many

        for field in fields:
            if field.name in disallowed:
                continue
            fieldsets[field.formfield().__class__.__name__].append(field.name)

        return (
            (name, {"fields": fields}) for name, fields in fieldsets.items()
        )
