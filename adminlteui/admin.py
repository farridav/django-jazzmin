import json

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import widgets
from django.core.files.storage import default_storage
from django.http.response import HttpResponse, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.urls import path, reverse, NoReverseMatch
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Options, Menu, ContentType
from .widgets import AdminlteSelect


class ImageBox:
    # for ClearableFileInput initial
    def __init__(self, name):
        self.url = f'{settings.MEDIA_URL}/{name}'
        self.value = name

    def __str__(self):
        return f'{self.value}'


class GeneralOptionForm(forms.Form):
    site_title = forms.CharField(
        label=_('Site Title'), widget=widgets.AdminTextInputWidget(),
        help_text=_("Text to put at the end of each page's tag title.")
    )
    site_header = forms.CharField(
        label=_('Site Header'), widget=widgets.AdminTextInputWidget(),
        help_text=_("Text to put in base page's tag b.")
    )
    # index_title = forms.CharField(label=_('Index Title'), widget=widgets.AdminTextInputWidget())
    site_logo = forms.ImageField(
        label=_('Site Logo'), widget=forms.ClearableFileInput(), required=False,
        help_text=_("Transparent background picture is a good choice.")
    )
    welcome_sign = forms.CharField(
        label=_('Welcome Sign'), widget=widgets.AdminTextInputWidget(),
        help_text=_("Login page welcome sign.")
    )
    avatar_field = forms.CharField(
        label=_('Avatar Field'), widget=widgets.AdminTextInputWidget(),
        required=False, help_text=_("which field is avatar.")
    )
    show_avatar = forms.BooleanField(label=_('Show Avatar'), required=False)

    def save(self):
        cleaned_data = self.cleaned_data
        options = Options.objects.in_bulk(field_name='option_name')

        if self.files.get('site_logo'):
            file = self.files['site_logo']
            cleaned_data['site_logo'] = default_storage.save(file.name, file)
        elif options.get('site_logo'):
            cleaned_data['site_logo'] = options.get('site_logo').option_value
        else:
            cleaned_data['site_logo'] = ''

        if self.data.get('site_logo-clear'):
            Options.objects.filter(option_name='site_logo').delete()
            cleaned_data['site_logo'] = ''

        cleaned_data['show_avatar'] = 'on' if cleaned_data.get('show_avatar') else 'off'

        for key, value in cleaned_data.items():
            option = options.get(key, Options(option_name=key, option_value=value))

            if not option.pk or option.option_value != value:
                option.option_value = value
                option.save()

        return cleaned_data


@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('option_name', 'valid', 'update_time', 'create_time')
    search_fields = ('option_name', 'option_value')
    list_filter = ('valid',)
    list_editable = ('valid',)

    def get_urls(self):
        base_urls = super().get_urls()
        urls = [
            path(
                'general_option/', self.admin_site.admin_view(self.general_option_view, cacheable=True),
                name='general_option'
            )
        ]
        return urls + base_urls

    def general_option_view(self, request):
        perms = ['django_admin_settings.add_options', 'django_admin_settings.change_options']
        if not all(request.user.has_perm(perm) for perm in perms):
            return HttpResponseForbidden(format_html('<h1>403 Forbidden</h1>'))

        context = dict(self.admin_site.each_context(request), )
        options = dict(Options.objects.values_list('option_name', 'option_value'))

        if request.method == 'POST':
            form = GeneralOptionForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                options = form.save()
                messages.add_message(request, messages.SUCCESS, _('General Option Saved.'))
            else:
                messages.add_message(request, messages.ERROR, _('General Option Save Failed.'))

        logo = options.get('site_logo')
        context['line'] = GeneralOptionForm(initial={
            'site_title': options.get('site_title', admin.AdminSite.site_title),
            'site_header': options.get('site_header', admin.AdminSite.site_header),
            # 'index_title': options.get('index_title', admin.AdminSite.index_title),
            'welcome_sign': options.get('welcome_sign'),
            'site_logo': ImageBox(logo) if logo else '',
            'show_avatar': True if options.get('show_avatar') == 'on' else False,
            'avatar_field': options.get('avatar_field', 'request.user.head_avatar'),
        })

        return TemplateResponse(request, 'adminlte/general_option.html', context)


@admin.register(Menu)
class MenuAdmin(TreeAdmin):
    list_display = (
        'name', 'position', 'link_type', 'display_link', 'display_content_type',
        'priority_level', 'display_icon', 'valid'
    )
    list_filter = ('position', 'link_type', 'valid')
    list_editable = ('valid', 'priority_level')
    form = movenodeform_factory(Menu)
    change_list_template = 'adminlte/menu_change_list.html'
    change_form_template = 'adminlte/menu_change_form.html'

    class ContentTypeModelChoiceField(forms.ModelChoiceField):

        def label_from_instance(self, obj):
            return f"{obj.app_label}:{obj.model}"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        reset content_type display text
        """
        if db_field.name == 'content_type':
            return self.ContentTypeModelChoiceField(
                queryset=ContentType.objects.all(), required=False, label=_('ContentType'), widget=AdminlteSelect
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        base_urls = super().get_urls()
        urls = [
            path(
                'exchange_menu/',
                self.admin_site.admin_view(self.exchange_menu_view, cacheable=True),
                name='exchange_menu'
            ),
        ]
        return urls + base_urls

    def exchange_menu_view(self, request):
        if not request.user.has_perm('django_admin_settings.view_menu'):
            return HttpResponseForbidden(format_html('<h1>403 Forbidden</h1>'))

        response_data = dict()
        response_data['message'] = 'success'
        use_custom_menu, _created = Options.objects.get_or_create(
            option_name='USE_CUSTOM_MENU', defaults={'option_value': '0'}
        )

        if use_custom_menu.option_value == '0':
            use_custom_menu.option_value = '1'
            use_custom_menu.save(update_fields=['option_value'])
            messages.add_message(request, messages.SUCCESS, _('Menu exchanged, current is "custom menu".'))

        else:
            use_custom_menu.option_value = '0'
            use_custom_menu.save(update_fields=['option_value'])

            messages.add_message(request, messages.SUCCESS, _('Menu exchanged, current is "system menu".'))

        return HttpResponse(json.dumps(response_data), content_type="application/json,charset=utf-8")

    def display_link(self, obj):
        if obj.link:
            if '/' in obj.link:
                return format_html(f'<i class="fa fa-check text-green"></i> {obj.link}')
            try:
                reverse(obj.link)
                return format_html(f'<i class="fa fa-check text-green"></i> {obj.link}')
            except NoReverseMatch:
                return format_html(f'<i class="fa fa-close text-red"></i> {obj.link}')
        return None

    display_link.short_description = _('Link')

    def display_icon(self, obj):
        if obj.icon:
            return format_html(f'<i class="fa {obj.icon}"></i> {obj.icon}')
        return obj.icon

    display_icon.short_description = _('Icon')

    def display_content_type(self, obj):
        if obj.content_type:
            return f'{obj.content_type.app_label}:{obj.content_type.model}'
        return obj.content_type_id

    display_content_type.short_description = _('ContentType')
