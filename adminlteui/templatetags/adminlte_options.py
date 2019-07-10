import traceback
from django import template
from adminlteui.models import Options
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_adminlte_option(option_name, request=None):
    config_ = {}
    config_list = Options.objects.filter(valid=True)

    if config_list.filter(option_name=option_name):
        config_[option_name] = config_list.get(
            option_name=option_name).option_value
        if request and option_name=='avatar_field':
            try:
                # request.user.head_avatar
                image_path = eval(config_[option_name]).name
                if image_path:
                    config_[option_name] = settings.MEDIA_URL + image_path
                else:
                    config_[option_name] = None
            except Exception as e:
                traceback.print_exc()
                config_[option_name] = None
        config_['valid'] = config_list.get(
            option_name=option_name).valid
    return config_
