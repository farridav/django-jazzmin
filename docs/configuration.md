# Configuration

To configure the general behaviour of jazzmin, you can use `JAZZMIN_SETTINGS` within your django settings, below is a 
full example, with some of the more complex items explained below that.

## Full example
```python
JAZZMIN_SETTINGS = {
    # title of the window
    'site_title': 'Polls Admin',

    # Title on the login screen
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
            'permissions': ['polls.view_polls']
        }]
    },

    # Custom icons per model in the side menu See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
    # for a list of icon classes
    'icons': {
        'auth.user': 'fa-user',
    }
}
```

## Top menu
You can enable the top menu by specifying `'topmenu_links'` in your `JAZZMIN_SETTINGS`, this is a list made up of one of:

 - app (creates a dropdown of modeladmin links)
 - model (creates a link to a modeladmin)
 - url (url name, or absolute link)

The top menu can be styled with the UI Customiser (See below)

## Side menu

### How its generated

The side menu gets a list of all installed apps and their models that have admin classes, and creates a tree of apps and 
links to model admin pages.

You can omit apps, or models from this generated menu, using `hide_apps` or `hide_models` where app is like `auth` and 
model is like `auth.user`

Ordering of the menu can be done using `order_with_respect_to`, which is a list of apps you want to base the ordering off 
of, it can be a partial list 

### Adding custom links

Custom links can be added using `custom_links`, this is a dictionary of links, keyed on the app they will live under. 
Example:

    'custom_links': {
        'polls': [{
            # Any Name you like
            'name': 'Make Messages',                
            
            # url name e.g `admin:index`, relative urls e.g `/admin/index` or absolute urls e.g `https://domain.com/admin/index`
            'url': 'make_messages',                 
            
            # any font-awesome icon, [see list here](https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/) (optional)
            'icon': 'fa-comments',                  
            
            # a list of permissions the user must have to see this link (optional)
            'permissions': ['polls.view_polls']     
        }]
    },

!!! note

    The app list you generate for the side menu, is shared with the dashboard, so any changes you make to it, will be 
    reflected there

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

Into your jazzmin settings (Ensure these files can be found by the static file finder), and the 
