import os

import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = 'x*za6xf&_80ofdpae!yzq61g9ffikkx9$*iygbl$j7rr4wlf8t'
DEBUG = True

ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tests.test_app.polls.apps.PollsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if django.VERSION < (2, 0):
    MIDDLEWARE_CLASSES = MIDDLEWARE

ROOT_URLCONF = 'tests.test_app.urls'

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

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    'topmenu_links': [

        # Url that gets reversed (Permissions can be added)
        {'name': 'Home', 'url': 'admin:index', 'permissions': ['auth.view_user']},

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

    # List of apps to base side menu ordering off of
    'order_with_respect_to': ['accounts', 'polls'],

    # Custom links to append to app groups, keyed on app name
    'custom_links': {
        'polls': [{
            'name': 'Make Messages', 'url': 'make_messages', 'icon': 'fa-comments',
            'permissions': ['polls.view_poll']
        }]
    },

    # Custom icons per model in the side menu See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
    # for a list of icon classes
    'icons': {
        'auth.user': 'fa-user',
    },

    #############
    # UI Tweaks #
    #############

    # Relative paths to custom CSS/JS scripts (must be present in static files)
    'custom_css': None,
    'custom_js': None,

    # Whether to show the UI customizer on the sidebar
    'show_ui_builder': False,
}

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': ':memory:'
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not os.getenv('FAIL_INVALID_TEMPLATE_VARS'):
    INSTALLED_APPS.extend([
        'debug_toolbar',
        'django_extensions',
    ])
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _: True}
