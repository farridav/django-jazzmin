import json
import traceback
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import widgets
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.conf import settings
from django.http.response import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest
from adminlteui.widgets import AdminlteSelect
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Options, Menu, ContentType


def get_option(option_name):
    try:
        if Options.objects.filter(option_name=option_name):
            return Options.objects.get(option_name=option_name).option_value
    except Exception:
        return None


def handle_uploaded_file(f, file_name):
    # save site_logo
    with open(settings.MEDIA_ROOT + '/' + file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class ImageBox:
    # for ClearableFileInput initial
    def __init__(self, name):
        self.url = '/' + name
        self.value = name

    def __str__(self):
        return '{}'.format(self.value)


def get_image_box():
    return ImageBox(get_option(option_name='site_logo')) if get_option(
        option_name='site_logo') else ''


class GeneralOptionForm(forms.Form):
    site_title = forms.CharField(label=_('Site Title'),
                                 widget=widgets.AdminTextInputWidget(),
                                 help_text=_(
                                     "Text to put at the end of each page's tag title."))
    site_header = forms.CharField(label=_('Site Header'),
                                  widget=widgets.AdminTextInputWidget(),
                                  help_text=_(
                                      "Text to put in base page's tag b."))
    # index_title = forms.CharField(label=_('Index Title'),
    #                               widget=widgets.AdminTextInputWidget())
    site_logo = forms.ImageField(label=_('Site Logo'),
                                 widget=forms.ClearableFileInput(),
                                 required=False,
                                 help_text=_(
                                     "Transparent background picture is a good choice."))
    welcome_sign = forms.CharField(
        label=_('Welcome Sign'),
        widget=widgets.AdminTextInputWidget(),
        help_text=_("Login page welcome sign.")
    )

    avatar_field = forms.CharField(label=_('Avatar Field'),
                                   widget=widgets.AdminTextInputWidget(),
                                   required=False,
                                   help_text=_(
                                       "which field is avatar."))
    show_avatar = forms.BooleanField(
        label=_('Show Avatar'), required=False)

    def save(self):
        try:
            # clear site-logo
            if self.data.get('site_logo-clear'):
                obj = Options.objects.get(option_name='site_logo')
                obj.delete()
                self.changed_data.remove('site_logo')

            if not self.data.get('show_avatar'):
                try:
                    obj = Options.objects.get(option_name='show_avatar')
                    obj.option_value = 'off'
                    obj.save()
                except Exception:
                    obj = Options.objects.create(option_name='show_avatar',
                                                 option_value='off')
                    obj.save()

            for data_item in self.changed_data:
                try:
                    obj = Options.objects.get(option_name=data_item)

                    if data_item == 'site_logo':
                        if not settings.MEDIA_ROOT or not settings.MEDIA_URL:
                            self.errors[data_item] = _(
                                'site_logo depends on setting.MEDIA_URL and setting.MEDIA_ROOT.')
                            return False
                        if not self.files.get(data_item) or self.data.get(
                                data_item) == '':
                            continue
                        handle_uploaded_file(self.files.get(data_item),
                                             self.files.get(data_item).name)
                        obj.option_value = settings.MEDIA_URL.lstrip(
                            '/') + self.files.get(
                            data_item).name
                    else:
                        if obj.option_value == self.data.get(data_item):
                            continue
                        obj.option_value = self.data.get(data_item)
                except Options.DoesNotExist:
                    if data_item == 'site_logo':
                        if not settings.MEDIA_ROOT or not settings.MEDIA_URL:
                            self.errors[data_item] = _(
                                'site_logo depends on setting.MEDIA_URL and setting.MEDIA_ROOT.')
                            return False
                        handle_uploaded_file(self.files.get(data_item),
                                             self.files.get(data_item).name)
                        obj = Options.objects.create(
                            option_name=data_item,
                            option_value=settings.MEDIA_URL.lstrip(
                                '/') + self.files.get(
                                data_item).name,
                            create_time=timezone.now())
                    else:
                        obj = Options.objects.create(
                            option_name=data_item,
                            option_value=self.data.get(data_item),
                            create_time=timezone.now())
                obj.save()
            return True

        except Exception as e:
            traceback.print_exc()
            # self.errors = e
            return False


@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('option_name', 'valid', 'update_time', 'create_time')
    search_fields = ('option_name', 'option_value')
    list_filter = ('valid',)
    list_editable = ('valid',)

    def get_urls(self):
        base_urls = super().get_urls()
        urls = [
            path('general_option/',
                 self.admin_site.admin_view(
                     self.general_option_view,
                     cacheable=True), name='general_option'),
        ]
        return urls + base_urls

    def general_option_view(self, request):
        if request.user.has_perm('django_admin_settings.add_options') is False \
                and request.user.has_perm(
            'django_admin_settings.change_options') is False:
            return HttpResponseForbidden(format_html('<h1>403 Forbidden</h1>'))

        context = dict(
            self.admin_site.each_context(request),
        )

        if request.method == 'GET':
            initial_value = {
                'site_title': get_option(
                    option_name='site_title') or admin.AdminSite.site_title,
                'site_header': get_option(
                    option_name='site_header') or admin.AdminSite.site_header,
                # 'index_title': get_option(
                #     option_name='index_title') or admin.AdminSite.index_title,
                'welcome_sign': get_option(option_name='welcome_sign'),
                'site_logo': ImageBox(
                    get_option(option_name='site_logo')) if get_option(
                    option_name='site_logo') else '',
                'show_avatar': True if get_option(
                    option_name='show_avatar') == 'on' else False,
                'avatar_field': get_option(
                    option_name='avatar_field') or 'request.user.head_avatar',
            }
            form = GeneralOptionForm(initial=initial_value)
        else:
            form = GeneralOptionForm(
                request.POST, request.FILES
            )

            if form.save():
                initial_value = {
                    'site_title': get_option(
                        option_name='site_title') or admin.AdminSite.site_title,
                    'site_header': get_option(
                        option_name='site_header') or admin.AdminSite.site_header,
                    # 'index_title': get_option(
                    #     option_name='index_title') or admin.AdminSite.index_title,
                    'welcome_sign': get_option(option_name='welcome_sign'),
                    'site_logo': ImageBox(
                        get_option(option_name='site_logo')) if get_option(
                        option_name='site_logo') else '',
                    'show_avatar': True if get_option(
                        option_name='show_avatar') == 'on' else False,
                    'avatar_field': get_option(
                        option_name='avatar_field') or 'request.user.head_avatar',
                }
                form = GeneralOptionForm(initial=initial_value)
                messages.add_message(request, messages.SUCCESS,
                                     _('General Option Saved.'))
            else:
                messages.add_message(request, messages.ERROR,
                                     _('General Option Save Failed.'))
        context['line'] = form
        return TemplateResponse(request, 'adminlte/general_option.html',
                                context)


@admin.register(Menu)
class MenuAdmin(TreeAdmin):
    list_display = ('name', 'position', 'link_type', 'display_link',
                    'display_content_type', 'priority_level', 'display_icon',
                    'valid')
    list_filter = ('position', 'link_type', 'valid')
    list_editable = ('valid', 'priority_level')
    form = movenodeform_factory(Menu)
    change_list_template = 'adminlte/menu_change_list.html'
    change_form_template = 'adminlte/menu_change_form.html'

    class ContentTypeModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return "%s:%s" % (obj.app_label, obj.model)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        reset content_type display text
        """
        if db_field.name == 'content_type':
            return self.ContentTypeModelChoiceField(
                queryset=ContentType.objects.all(),
                required=False,
                label=_('ContentType'),
                widget=AdminlteSelect)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            return super().changeform_view(request, object_id, form_url, extra_context)
        except Exception as e:
            messages.error(request,
                           _('Exception raised while add node: %s') % _(
                               force_str(e)))
            return HttpResponseBadRequest(
                _('Exception raised while add node: %s') % _(force_str(e)))

    def get_urls(self):
        base_urls = super().get_urls()
        urls = [
            path('exchange_menu/',
                 self.admin_site.admin_view(
                     self.exchange_menu_view,
                     cacheable=True), name='exchange_menu'),
        ]
        return urls + base_urls

    def exchange_menu_view(self, request):
        if request.user.has_perm('django_admin_settings.view_menu') is False:
            return HttpResponseForbidden(format_html('<h1>403 Forbidden</h1>'))
        if request.is_ajax():
            response_data = dict()
            response_data['message'] = 'success'
            try:
                use_custom_menu = Options.objects.get(
                    option_name='USE_CUSTOM_MENU')
            except Options.DoesNotExist:
                use_custom_menu = Options.objects.create(
                    option_name='USE_CUSTOM_MENU', option_value='0'
                )

            if not use_custom_menu or use_custom_menu.option_value == '0':
                use_custom_menu.option_value = '1'
                use_custom_menu.save()
                messages.add_message(request, messages.SUCCESS, _(
                    'Menu exchanged, current is `custom menu`.'))

            else:
                use_custom_menu.option_value = '0'
                use_custom_menu.save()
                messages.add_message(request, messages.SUCCESS, _(
                    'Menu exchanged, current is `system menu`.'))
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json,charset=utf-8")
        return HttpResponse('method not allowed.')

    def display_link(self, obj):
        if obj.link:
            if '/' in obj.link:
                return format_html(
                    '<i class="fa fa-check text-green"></i> {}'.format(
                        obj.link))
            try:
                reverse(obj.link)
                return format_html(
                    '<i class="fa fa-check text-green"></i> {}'.format(
                        obj.link))
            except Exception as e:
                return format_html(
                    '<i class="fa fa-close text-red"></i> {}'.format(obj.link))
        return '-'

    display_link.short_description = _('Link')

    def display_icon(self, obj):
        if obj.icon:
            return format_html(
                '<i class="fa {}"></i> {}'.format(obj.icon, obj.icon))
        return obj.icon

    display_icon.short_description = _('Icon')

    def display_content_type(self, obj):
        if obj.content_type:
            return '{}:{}'.format(obj.content_type.app_label,
                                  obj.content_type.model)
        return obj.content_type_id

    display_content_type.short_description = _('ContentType')
