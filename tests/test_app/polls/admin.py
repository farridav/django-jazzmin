from django.contrib import admin

from .models import Poll, Choice, Vote


class ChoiceInline(admin.TabularInline):
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
