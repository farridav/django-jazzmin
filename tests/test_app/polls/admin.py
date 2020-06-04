from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django.utils.timesince import timesince

from .models import Poll, Choice, Vote


class ChoiceInline(admin.StackedInline):
    model = Choice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    fieldsets = (
        ('general', {'fields': ('owner',)}),
        ('other', {'fields': ('text', 'pub_date', 'active')})
    )
    raw_id_fields = ('owner',)
    list_display = ('owner', 'text', 'pub_date', 'active')
    list_display_links = ()
    list_filter = ('active', 'owner')
    list_select_related = False
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ('active',)
    search_fields = ('text', 'owner__email')
    date_hierarchy = 'pub_date'
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
    list_display = ('poll', 'choice_text')
    list_per_page = 20
    list_editable = ('choice_text',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'choice')


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'object', 'action_flag', 'change_message', 'modified')
    readonly_fields = ['object', 'modified']
    search_fields = ('user__email',)
    date_hierarchy = 'action_time'
    list_filter = ('action_flag', 'content_type__model')
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
            return 'Never'
        return '{} ago'.format(timesince(obj.action_time))

    modified.admin_order_field = 'action_time'
