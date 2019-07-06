# Guides

## General Option

dynamic setup your site base on table `django_admin_settings_options`.

support options:

- Site Title
- Site Header
- Site Logo
- Welcome Sign

## Options

this options in your db, named `django_admin_settings_options`, after do migrate.

you can also add your custom option into this table, and use it by templatetags
 `adminlte_options` with function `get_adminlte_option`.

options table has a valid field to control your option work or not.


example:

```
# adminlte/general_option.html

{% load adminlte_options %}

# here my option_name is site_title, you can custom yourself.
{% get_adminlte_option 'site_title' as adminlte_site_title %}
{% if adminlte_site_title.valid %}
{{ adminlte_site_title.site_title }}
{% else %}
{{ site_title|default:_('Django site admin') }}
{% endif %}

```

before custom option, you should known what adminlte has used.

- site_title
- site_header
- site_logo
- welcome_sign

## Widgets

### AdminlteSelect

example:
```
# adminlte/admin.py
@admin.register(Menu)
class MenuAdmin(TreeAdmin):
    ...
    change_form_template = 'adminlte/menu_change_form.html'
    formfield_overrides = {
        models.ForeignKey: {'widget': AdminlteSelect}
    }

# adminlte/menu_change_form.html
# active the target select
{% extends 'admin/change_form.html' %}

{% block extrajs %}
{{ block.super }}
<script>
    django.jQuery('#id_content_type').select2();
</script>
{% endblock %}
```
effect:

![adminlte_select](https://github.com/wuyue92tree/django-adminlte-ui/blob/master/images/adminlte_select.png?raw=true)

### AdminlteSelectMultiple

example:
```
# adminlte/admin.py
@admin.register(Menu)
class MenuAdmin(TreeAdmin):
    ...
    change_form_template = 'adminlte/menu_change_form.html'
    formfield_overrides = {
        # multiple for ManayToManyField
        models.ManayToManyField: {'widget': AdminlteSelectMultiple(
            attr={'style': 'width: 100%'}
        )}
    }

# adminlte/menu_change_form.html
# active the target select
{% extends 'admin/change_form.html' %}

{% block extrajs %}
{{ block.super }}
<script>
    django.jQuery('#id_content_type').select2();
</script>
{% endblock %}
```
effect:

![adminlte_select](https://github.com/wuyue92tree/django-adminlte-ui/blob/master/images/adminlte_select_multiple.png?raw=true)



## Menu

developing ...
