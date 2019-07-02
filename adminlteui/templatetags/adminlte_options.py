from django import template
from adminlteui.models import Options

register = template.Library()


@register.simple_tag
def get_adminlte_option(option_name):
    config_ = {}
    config_list = Options.objects.filter(valid=True)

    if config_list.filter(option_name=option_name):
        config_[option_name] = config_list.get(
            option_name=option_name).option_value
        config_['valid'] = config_list.get(
            option_name=option_name).valid
    return config_
