import traceback
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import widgets
from django.urls import path
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db import models
from django.conf import settings
from adminlteui.widgets import AdminlteSelect, AdminlteSelectMultiple
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Options, Menu


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

    def save(self):
        try:
            # clear site-logo
            if self.data.get('site_logo-clear'):
                obj = Options.objects.get(option_name='site_logo')
                obj.delete()
                self.changed_data.remove('site_logo')

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
                    option_name='site_logo') else ''
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
                        option_name='site_logo') else ''
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
    list_display = ('name', 'position', 'link_type', 'link',
                    'content_type', 'display_icon',
                    'valid')
    list_filter = ('position', 'link_type', 'valid')
    list_editable = ('valid',)
    form = movenodeform_factory(Menu)
    change_list_template = 'adminlte/menu_change_list.html'
    change_form_template = 'adminlte/menu_change_form.html'
    formfield_overrides = {
        models.ForeignKey: {'widget': AdminlteSelect}
    }

    def display_icon(self, obj):
        if obj.icon:
            return format_html(
                '<i class="fa {}"></i> {}'.format(obj.icon, obj.icon))
        return obj.icon

    display_icon.short_description = _('Icon')
