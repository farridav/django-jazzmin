# UI Tweaks

There are various things you can do to change the look and feel of your admin when using jazzmin, some are structural
changes

## UI Customizer

Jazzmin has a built in UI configurator, mimicked + enhanced from [adminlte demo](https://adminlte.io/themes/v3/index3.html),
that allows you to customise parts of the interface interactively.

To enable this, set `JAZZMIN_SETTINGS["show_ui_builder"] = True` and there will be an icon in the top right of the screen
that allows you to customise the interface.

![icon](./img/customise_icon.png)

When your happy with your customisations, press the "Show Code" button, and it will give you a code snippet to put
into your settings that will persist these customisations beyond page refresh.

## Themes

With the ui customiser enabled (see above), you can try out different bootswatch themes, and combine the theme with our
other UI tweaks.

### Dark mode enabled

If you set `JAZZMIN_UI_TWEAKS["dark_mode_theme"]` to a dark theme, then users that have opted for dark mode on their
device will be served this theme instead of the one in `JAZZMIN_UI_TWEAKS["theme"]`

This is done using `prefers-color-scheme` in the CSS media attribute, see [here](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme)
for more information on the web standard

for example, to use `flatly` for all users that have no preference or prefer light mode, and `darkly` for those who opt
for dark mode on their device:

```python
JAZZMIN_UI_TWEAKS = {
    ...
    "theme": "flatly",
    "dark_mode_theme": "darkly",
}
```

To force the use of a single theme regardless, just omit `dark_mode_theme` from your `JAZZMIN_UI_TWEAKS`

You can preview any of the available themes on your site using the UI Customizer (See above), or view them on bootswatch
below

### Light themes

- default (Standard theme built on top of bootstrap)
- cerulean [preview](https://bootswatch.com/cerulean/)
- cosmo [preview](https://bootswatch.com/cosmo/)
- flatly [preview](https://bootswatch.com/flatly/)
- journal [preview](https://bootswatch.com/journal/)
- litera [preview](https://bootswatch.com/litera/)
- lumen [preview](https://bootswatch.com/lumen/)
- lux [preview](https://bootswatch.com/lux/)
- materia [preview](https://bootswatch.com/materia/)
- minty [preview](https://bootswatch.com/minty/)
- pulse [preview](https://bootswatch.com/pulse/)
- sandstone [preview](https://bootswatch.com/sandstone/)
- simplex [preview](https://bootswatch.com/simplex/)
- sketchy [preview](https://bootswatch.com/sketchy/)
- spacelab [preview](https://bootswatch.com/spacelab/)
- united [preview](https://bootswatch.com/united/)
- yeti [preview](https://bootswatch.com/yeti/)

### Dark themes

- darkly [preview](https://bootswatch.com/darkly/)
- cyborg [preview](https://bootswatch.com/cyborg/)
- slate [preview](https://bootswatch.com/slate/)
- solar [preview](https://bootswatch.com/solar/)
- superhero [preview](https://bootswatch.com/superhero/)

Here are some screenshots of the themes in action, Use the UI Customizer (See above) to test them all

### Darkly

```python
JAZZMIN_UI_TWEAKS = {
    ...
    "theme": "darkly",
}
```

![icon](./img/theme_darkly.png)

### Simplex

```python
JAZZMIN_UI_TWEAKS = {
    ...
    "theme": "simplex",
}
```

![icon](./img/theme_simplex.png)

### Sketchy

```python
JAZZMIN_UI_TWEAKS = {
    ...
    "theme": "sketchy",
}
```

![icon](./img/theme_sketchy.png)

### Slate

```python
JAZZMIN_UI_TWEAKS = {
    ...
    "theme": "slate",
}
```

![icon](./img/theme_slate.png)

## DIY with custom CSS/JS

If there are things you need to do with CSS/JS, but want to avoid overriding the templates yourself, you can include a
custom CSS and/or JS file, just pass a relative path to your files e.g:

```python
"custom_css": "common/css/main.css",
"custom_js": "common/js/main.js"
```

Into your jazzmin settings (Ensure these files can be found by the static file finder)

If you want to manually tweak CSS styles for a particular theme, you can start your CSS rule with
`body.theme-<themename>` e.g:

```css
body.theme-darkly p {
    color: pink;
}
```

Or to target your `dark_mode_theme` wrap it like this:

```css
@media (prefers-color-scheme: dark) {
    body.theme-darkly p {
        color: pink;
    }
}
```

## Custom Menu

The custom menu feature allows you to manually craft the side menu using an app-to-model mapping instead of generating a menu based on installed apps. This provides more control over the structure and organization of the admin interface.

### Configuration

To enable and configure the custom menu, follow these steps:

1. **Enable Custom Menu in Settings**
   Add the `custom_menu` setting in your `jazzmin/settings.py` file. This setting should be a dictionary where the keys are app labels or arbitrary group names, and the values are lists of model names.

    Example configuration:
    ```python
    JAZZMIN_SETTINGS = {
        # other settings...
        
        # Do not generate a menu based off of installed apps, instead manually craft one using this app -> model mapping
        "custom_menu": {
            "auth": ["books.book"],  # Group 'auth' with model 'books.book'
            "arbitrary_name": ["auth.user", "auth.group"]  # Custom group with 'auth.user' and 'auth.group'
        },

        # other settings...
    }
    ```

2. **Customize Menu Appearance**
   You can also customize the icons for your apps and models using the `icons` setting. This allows for a visually distinct menu.

    Example configuration:
    ```python
    JAZZMIN_SETTINGS = {
        # other settings...
        
        # Custom icons for side menu apps/models
        "icons": {
            # other settings...
            "arbitrary_name.user": "fas fa-user",
            "arbitrary_name.group": "fas fa-users"
        },

        # other settings...
    }
    ```
