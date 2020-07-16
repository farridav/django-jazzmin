# Configuration

To configure the general behaviour of jazzmin, you can use `JAZZMIN_SETTINGS` within your django settings, below is a 
full example, with some of the more complex items explained below that.

## Full example
```python
JAZZMIN_SETTINGS = {
    # title of the window
    'site_title': 'Polls Admin',

    # Title on the brand, and the login screen (19 chars max)
    'site_header': 'Polls',

    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    'site_logo': 'polls/img/logo.png',

    # Welcome text on the login screen
    'welcome_sign': 'Welcome to polls',

    # Copyright on the footer
    'copyright': 'Acme Ltd',

    # The model admin to search from the search bar, search bar omitted if excluded
    'search_model': 'auth.User',

    # Field name on user model that contains avatar image
    'user_avatar': None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    'topmenu_links': [

        # Url that gets reversed (Permissions can be added)
        {'name': 'Home',  'url': 'admin:index', 'permissions': ['auth.view_user']},

        # external url that opens in a new window (Permissions can be added)
        {'name': 'Support', 'url': 'https://github.com/farridav/django-jazzmin/issues', 'new_window': True},

        # model admin to link to (Permissions checked against model)
        {'model': 'auth.User'},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {'app': 'polls'},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    'usermenu_links': [
        {'name': 'Support', 'url': 'https://github.com/farridav/django-jazzmin/issues', 'new_window': True},
        {'model': 'auth.user'}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    'show_sidebar': True,

    # Whether to aut expand the menu
    'navigation_expanded': True,

    # Hide these apps when generating side menu e.g (auth)
    'hide_apps': [],

    # Hide these models when generating side menu (e.g auth.user)
    'hide_models': [],

    # List of apps to base side menu ordering off of (does not need to contain all apps)
    'order_with_respect_to': ['accounts', 'polls'],

    # Custom links to append to app groups, keyed on app name
    'custom_links': {
        'polls': [{
            'name': 'Make Messages', 
            'url': 'make_messages', 
            'icon': 'fa-comments',
            'permissions': ['polls.view_poll']
        }]
    },

    # Custom icons for side menu apps/models See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
    # for a list of icon classes
    'icons': {
        'auth': 'fa-users-cog',
        'auth.user': 'fa-user',
        'auth.Group': 'fa-users',
    },
    # Icons that are used when one is not manually specified
    'default_icon_parents': 'fa-chevron-circle-right',
    'default_icon_children': 'fa-circle',

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - accordion
    # - carousel
    "changeview_format": "horizontal_tabs",
}
```

## Top menu

![Top Menu](./img/top_menu.png)

You can enable the top menu by specifying `'topmenu_links'` in your `JAZZMIN_SETTINGS`, this is a list made up of one of:

 - app (creates a dropdown of modeladmin links)
 - model (creates a link to a modeladmin)
 - url (url name, or absolute link)

The top menu can be styled with the UI Customiser (See below)

## User menu
You can add links to the user menu on the top right of the screen using the `'usermenu_links'` settings key, the format 
of these links is the same as with top menu (above), though submenus via 'app' are not currently supported and will not 
be rendered.

![User Menu](./img/user_menu.png)
    
## Side menu

![Side Menu](./img/side_menu.png)

### How its generated

The side menu gets a list of all installed apps and their models that have admin classes, and creates a tree of apps and 
links to model admin pages.

You can omit apps, or models from this generated menu, using `hide_apps` or `hide_models` where app is like `auth` and 
model is like `auth.user`

Ordering of the menu can be done using `order_with_respect_to`, which is a list of apps you want to base the ordering off 
of, it can be a partial list 

### Side menu custom links

Custom links can be added using `custom_links`, this is a dictionary of links, keyed on the app they will live under. 
Example:

    'custom_links': {
        'polls': [{
            # Any Name you like
            'name': 'Make Messages',                
            
            # url name e.g `admin:index`, relative urls e.g `/admin/index` or absolute urls e.g `https://domain.com/admin/index`
            'url': 'make_messages',                 
            
            # any font-awesome icon, see list here https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/ (optional)
            'icon': 'fa-comments',                  
            
            # a list of permissions the user must have to see this link (optional)
            'permissions': ['polls.view_poll']     
        }]
    },

#### note
The app list you generate for the side menu, is shared with the dashboard, so any changes you make to it, will be reflected there

## Change form display
We have a few different styles for a model admins change form, currently, when applied, it affects all model admin change forms, 
though there are plans to allow overiding on a per model basis, like with other settings.

The default style is vertical tabs, *unless* you have no fieldsets and no inlines, in which case you will get the basic single form 
rendered out, See [Django docs](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets) 
on how to add fieldsets to your admin classes.

See below for the different styles:

### Single page (`single`)
Render the form out in one page, including inlines, plain and simple, closest to the original Django admin change form

![Single](./img/changeform_single.png)

### Horizontal tabs (`horizontal_tabs`)
Puts all fieldsets and inlines into tab panes with horizontal nav tab controls, this is the default view for change 
forms that have fieldsets. or an inline

![Horizontal tabs](./img/changeform_horizontal_tabs.png)

### Vertical tabs (`vertical_tabs`)
Puts each fieldset or inline in a separate pane, controlled by vertical tabs on the left hand side.

Future enhancement: Allow tabs to be on the left or right

![Vertical tabs](./img/changeform_vertical_tabs.png)

### Accordion (`accordion`)
Puts all fieldsets and inlines in bootstrap collapsables in an accordion, allows many collapsables to be open at the 
same time, the first accordion is opened

![Accordion](./img/changeform_accordion.png)

### Carousel (`carousel`)
Puts fieldsets and inlines into a bootstrap carousel, and allows paginaton with previous/nect buttons, as well as an indicators.

![Carousel](./img/changeform_carousel.png)

## UI Tweaks

### UI Customiser

Jazzmin has a built in UI configurator, mimicked from [adminlte demo](https://adminlte.io/themes/v3/index3.html), 
that allows you to customise parts of the interface interactively.

To enable this, add `'show_ui_builder': True` to your `JAZZMIN_SETTINGS` and there will be an icon in the top right of 
the screen that allows you to customise the interface.

![icon](./img/customise_icon.png)

When your happy with your customisations, press the "Show Code" button, and it will give you a code snippet to put 
into your settings that will persist these customisations beyond page refresh.

### DIY with custom CSS/JS

If there are things you need to do with CSS/JS, but want to avoid overriding the templates yourself, you can include a 
custom CSS and/or JS file, just pass a relative path to your files e.g:

```
'custom_css': 'common/css/main.css',
'custom_js': 'common/js/main.js'
 ```

Into your jazzmin settings (Ensure these files can be found by the static file finder)
