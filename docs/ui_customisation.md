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

### Color scheme (light / dark)

Any Bootswatch theme can be shown in light or dark. Jazzmin sets Bootstrap’s `data-bs-theme` on the `<html>` element
to `"light"` or `"dark"`, so the same theme adapts to the chosen color scheme.

- **`default_theme_mode`** in `JAZZMIN_UI_TWEAKS`: `"light"`, `"dark"`, or `"auto"`. With `"auto"`, the scheme follows
  the system preference (`prefers-color-scheme`). Default is `"light"`.
- The UI customizer lets users switch between Light, Dark, and System; the choice is stored in `localStorage` and can be
  copied into settings via “Show code”.

Example: default to dark, with one theme for everyone:

```python
JAZZMIN_UI_TWEAKS = {
    ...
    "theme": "flatly",
    "default_theme_mode": "dark",
}
```

Example: follow system preference:

```python
JAZZMIN_UI_TWEAKS = {
    ...
    "theme": "flatly",
    "default_theme_mode": "auto",
}
```

**Migration from `dark_mode_theme`:** If you had `dark_mode_theme` set (e.g. `"darkly"`), it is deprecated and no longer used. For the same behaviour (dark theme when the user’s system prefers dark), set `default_theme_mode": "auto"` and remove `dark_mode_theme`. If you do not update your config, Jazzmin will treat existing `dark_mode_theme` as `default_theme_mode": "auto"` and log a deprecation warning.

You can preview any of the available themes on your site using the UI Customizer (see above), or view them on bootswatch
below.

### Available themes

- default (standard Bootstrap-based theme)
- brite [preview](https://bootswatch.com/brite/)
- cerulean [preview](https://bootswatch.com/cerulean/)
- cosmo [preview](https://bootswatch.com/cosmo/)
- cyborg [preview](https://bootswatch.com/cyborg/)
- darkly [preview](https://bootswatch.com/darkly/)
- flatly [preview](https://bootswatch.com/flatly/)
- journal [preview](https://bootswatch.com/journal/)
- litera [preview](https://bootswatch.com/litera/)
- lumen [preview](https://bootswatch.com/lumen/)
- lux [preview](https://bootswatch.com/lux/)
- materia [preview](https://bootswatch.com/materia/)
- minty [preview](https://bootswatch.com/minty/)
- morph [preview](https://bootswatch.com/morph/)
- pulse [preview](https://bootswatch.com/pulse/)
- quartz [preview](https://bootswatch.com/quartz/)
- sandstone [preview](https://bootswatch.com/sandstone/)
- simplex [preview](https://bootswatch.com/simplex/)
- sketchy [preview](https://bootswatch.com/sketchy/)
- slate [preview](https://bootswatch.com/slate/)
- solar [preview](https://bootswatch.com/solar/)
- spacelab [preview](https://bootswatch.com/spacelab/)
- superhero [preview](https://bootswatch.com/superhero/)
- united [preview](https://bootswatch.com/united/)
- vapor [preview](https://bootswatch.com/vapor/)
- yeti [preview](https://bootswatch.com/yeti/)
- zephyr [preview](https://bootswatch.com/zephyr/)

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

To target dark color scheme (when `data-bs-theme="dark"` is set on the document), use:

```css
html[data-bs-theme="dark"] body.theme-darkly p {
    color: pink;
}
```
