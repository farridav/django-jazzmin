import os

import dj_database_url

###################
# Django Settings #
###################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "not-secret-at-all")
DEBUG = bool(int(os.getenv("DEBUG", 1)))
TEST = os.getenv("FAIL_INVALID_TEMPLATE_VARS")

PREFIX = "" if os.getenv("STANDALONE") else "tests.test_app."

ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    # Keep this above 'django.contrib.admin'
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "import_export",
    # Our apps
    "{}library.books.apps.BooksConfig".format(PREFIX),
    "{}library.loans.apps.LoansConfig".format(PREFIX),
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "{}library.urls".format(PREFIX)

WSGI_APPLICATION = "{}library.wsgi.application".format(PREFIX)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"": {"handlers": ["console"], "level": "INFO"}},
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

DATABASES = {
    "default": dj_database_url.config(
        env="DATABASE_URL", conn_max_age=500, default="sqlite:///{}".format(os.path.join(BASE_DIR, "db.sqlite3")),
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/London"
USE_I18N = True
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
USE_L10N = True
USE_TZ = True

# English default
gettext = lambda s: s  # NOQA
LANGUAGES = (
    ("en", gettext("English")),
    ("de", gettext("German")),
    ("es", gettext("Spanish")),
    ("hu", gettext("Hungarian")),
    ("zh-hans", gettext("Simplified Chinese")),
    ("zh-hant", gettext("Traditional Chinese")),
)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

if DEBUG and not TEST:
    os.environ.setdefault("WERKZEUG_DEBUG_PIN", "off")
    INSTALLED_APPS.extend(["debug_toolbar", "django_extensions"])
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _: False}

if not DEBUG and not TEST:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

########################
# Third party settings #
########################
JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "Library Admin",
    # Title on the brand, and the login screen (19 chars max)
    "site_header": "Library",
    # square logo to use for your site, must be present in static files, used for favicon and brand on top left
    "site_logo": "books/img/logo.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the library",
    # Copyright on the footer
    "copyright": "Acme Library Ltd",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "auth.User",
    # Field name on user model that contains avatar image
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True,},
        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "books"},
        {"app": "loans"},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True,},
        {"model": "auth.user"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps to base side menu (app or model) ordering off of
    "order_with_respect_to": ["Make Messages", "auth", "books", "books.author", "books.book", "loans",],
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "loans": [
            {
                "name": "Make Messages",
                "url": "make_messages",
                "icon": "fas fa-comments",
                "permissions": ["loans.view_loan"],
            }
        ]
    },
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free
    # for a list of icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file",
        "books.Author": "fas fa-user",
        "books.Book": "fas fa-book",
        "books.Genre": "fas fa-photo-video",
        "loans.BookLoan": "fas fa-book-open",
        "loans.Library": "fas fa-book-reader",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Activate Bootstrap modal
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs",},
    # Add a language dropdown into the admin
    "language_chooser": True,
}

if not DEBUG and not TEST:
    JAZZMIN_SETTINGS["welcome_sign"] = "Username: test@test.com, Password: test (Data resets nightly)"

################
# App settings #
################
