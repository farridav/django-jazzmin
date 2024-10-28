from enum import StrEnum
from functools import cached_property
from typing import Annotated, Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, BeforeValidator, Field, computed_field

from .utils import get_admin_url, get_model_meta
from .validators import validate_app, validate_app_or_model, validate_model, validate_static_file

App = Annotated[str, BeforeValidator(validate_app)]
Model = Annotated[str, BeforeValidator(validate_model)]
AppOrModel = Annotated[App | Model, BeforeValidator(validate_app_or_model)]
StaticFile = Annotated[str, BeforeValidator(validate_static_file)]


class MenuLink(BaseModel):
    name: Optional[str] = None
    url: str = "#"
    permissions: List[str] = []
    new_window: bool = False
    model: Optional[Model] = None
    app: Optional[App] = None
    icon: Optional[str] = None


class ChangeFormTemplate(StrEnum):
    single = "single"
    carousel = "carousel"
    collapsible = "collapsible"
    horizontal_tabs = "horizontal_tabs"
    vertical_tabs = "vertical_tabs"

    @staticmethod
    def get_template(choice: "ChangeFormTemplate") -> str:
        return f"jazzmin/includes/{choice.name}.html"


class DarkTheme(StrEnum):
    darkly = "darkly"
    cyborg = "cyborg"
    slate = "slate"
    solar = "solar"
    superhero = "superhero"


class Theme(StrEnum):
    # light themes
    default = "default"
    cerulean = "cerulean"
    cosmo = "cosmo"
    flatly = "flatly"
    journal = "journal"
    litera = "litera"
    lumen = "lumen"
    lux = "lux"
    materia = "materia"
    minty = "minty"
    pulse = "pulse"
    sandstone = "sandstone"
    simplex = "simplex"
    sketchy = "sketchy"
    spacelab = "spacelab"
    united = "united"
    yeti = "yeti"
    darkly = "darkly"
    cyborg = "cyborg"
    slate = "slate"
    solar = "solar"
    superhero = "superhero"

    @staticmethod
    def get_theme(choice: "ChangeFormTemplate") -> str:
        return f"vendor/bootswatch/{choice.name}/bootstrap.min.css"

    def is_dark(self) -> bool:
        return self in DarkTheme.__members__.values()


class SearchModel(BaseModel):
    search_name: str
    search_url: str


class JazzminSettings(BaseModel):
    site_title: Optional[str] = Field(
        default=None,
        description="Title of the window (Will default to current_admin_site.site_title)",
        examples=["My Admin"],
    )
    site_header: Optional[str] = Field(
        default=None,
        description="Title on the login screen (19 chars max) (will default to current_admin_site.site_header)",
        examples=["My Admin"],
    )
    site_brand: Optional[str] = Field(
        default=None,
        description="Title on the brand (19 chars max) (will default to current_admin_site.site_header)",
        le=19,
        examples=["My Admin"],
    )
    site_logo: str = Field(
        default="vendor/adminlte/img/AdminLTELogo.png",
        description="Relative path to logo for your site, used for brand on top left (must be present in static files)",
        examples=["vendor/adminlte/img/AdminLTELogo.png"],
    )
    login_logo: Optional[StaticFile] = Field(
        default=None,
        description="""
        Relative path to logo for your site, used for login logo (must be present in static files.
        Defaults to the same as site_logo
        """,
        examples=["vendor/adminlte/img/AdminLTELogo.png"],
    )
    login_logo_dark: Optional[StaticFile] = Field(
        default=None,
        description="""
        Logo to use for login form in dark themes (must be present in static files. Defaults to login_logo)
        """,
        examples=["vendor/adminlte/img/AdminLTELogo.png"],
    )
    site_logo_classes: str = Field(default="img-circle", description="CSS classes that are applied to the logo")
    site_icon: Optional[StaticFile] = Field(
        default=None,
        description="Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)",
    )
    welcome_sign: str = Field(default="Welcome", description="Welcome text on the login screen")
    copyright: str = Field(default="", description="Copyright on the footer")
    search_models: List[Model] = Field(
        default=[],
        description="The models to search from the search bar, search bar omitted if excluded",
        examples=["auth.User", "auth.Group"],
    )
    user_avatar: Optional[Union[str, Callable[..., str]]] = Field(
        default=None,
        description="""
        Field name on user model that contains avatar ImageField/URLField/Charfield
        or a callable that receives the user and returns the avatar url
        """,
        examples=["avatar", "get_avatar_url"],
    )
    topmenu_links: List[MenuLink] = Field(
        default=[],
        description="Links to put along the nav bar",
        examples=[
            [
                MenuLink(name="Home", url="admin:index", permissions=["auth.view_user"]),
                MenuLink(name="Support", url="https://github.com/farridav/django-jazzmin/issues", new_window=True),
                MenuLink(model="auth.user"),
                MenuLink(app="books"),
                MenuLink(app="loans"),
            ]
        ],
    )
    usermenu_links: List[MenuLink] = Field(
        default=[],
        description="Additional links to include in the user menu on the top right ('app' url type is not allowed)",
        examples=[
            [
                MenuLink(name="Support", url="https://github.com/farridav/django-jazzmin/issues", new_window=True),
                MenuLink(model="auth.user"),
            ]
        ],
    )
    show_sidebar: bool = Field(default=True, description="Whether to display the side menu")
    navigation_expanded: bool = Field(default=True, description="Whether to aut expand the menu")
    hide_apps: List[App] = Field(
        default=[], description="Hide these apps when generating side menu e.g (auth)", examples=["auth"]
    )
    hide_models: List[Model] = Field(
        default=[], description="Hide these models when generating side menu (e.g auth.user)", examples=["auth.user"]
    )
    order_with_respect_to: List[AppOrModel | str] = Field(
        default_factory=list, description="List of apps to base side menu ordering off of"
    )
    custom_links: Dict[App | str, list[MenuLink]] = Field(
        default_factory=dict,
        description="""
        Custom links to append to side menu app groups, keyed on lower case app label or makes a new group if
        the given app label doesnt exist in installed apps
        """,
    )

    icons: Dict[AppOrModel, str] = Field(
        default={"auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users"},
        description="Custom icons for side menu apps/models",
    )
    default_icon_parents: str = Field(
        default="fas fa-chevron-circle-right",
        description="""
        Default icon that is used for app group when one is not manually specified
        """,
        examples=["fas fa-chevron-circle-right"],
    )
    default_icon_children: str = Field(
        default="fas fa-circle",
        description="""
        Default icon that is used for child items when one is not manually specified
        """,
    )
    related_modal_active: bool = Field(default=False, description="Activate Bootstrap modal")
    custom_css: Optional[StaticFile] = Field(
        default=None, description="Relative paths to custom CSS/JS scripts (must be present in static files)"
    )
    custom_js: Optional[StaticFile] = Field(
        default=None, description="Relative paths to custom CSS/JS scripts (must be present in static files)"
    )
    use_google_fonts_cdn: bool = Field(
        default=True,
        description="Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)",
    )
    show_ui_builder: bool = Field(default=False, description="Whether to show the UI customizer on the sidebar")
    changeform_format: ChangeFormTemplate = Field(
        default=ChangeFormTemplate.horizontal_tabs,
        description="Render out the change view as a single form, or in tabs",
    )
    changeform_format_overrides: Dict[Model, ChangeFormTemplate] = Field(
        default={},
        description="Override change forms on a per modeladmin basis",
        examples=[{"auth.user": ChangeFormTemplate.collapsible}],
    )
    language_chooser: bool = Field(default=False, description="Add a language dropdown into the admin")

    @computed_field
    @cached_property
    def search_models_parsed(self) -> List[SearchModel]:
        search_models: List[SearchModel] = []

        for search_model in self.search_models:
            model_meta = get_model_meta(search_model)
            search_url = get_admin_url(search_model)

            if model_meta and model_meta.verbose_name_plural:
                search_name = model_meta.verbose_name_plural.title()
            else:
                search_name = search_model.split(".")[-1] + "s"

            search_models.append(SearchModel(search_name=search_name, search_url=search_url))

        return search_models

    def get_login_logo(self) -> str:
        return self.login_logo or self.site_logo

    def get_login_logo_dark(self) -> str:
        return self.login_logo_dark or self.login_logo or self.site_logo


class ButtonClasses(BaseModel):
    primary: str = "btn-primary"
    secondary: str = "btn-secondary"
    info: str = "btn-info"
    warning: str = "btn-warning"
    danger: str = "btn-danger"
    success: str = "btn-success"


class ElementClasses(BaseModel):
    theme: Theme = Theme.default
    dark_mode_theme: Optional[Theme] = None
    raw: dict[str, Any] = {}
    sidebar_classes: list[str] = []
    navbar_classes: list[str] = []
    body_classes: list[str] = []
    actions_classes: list[str] = []
    sidebar_list_classes: list[str] = []
    brand_classes: list[str] = []
    footer_classes: list[str] = []
    button_classes: ButtonClasses = ButtonClasses()


class UITweaks(BaseModel):
    """
    Currently available UI tweaks, Use the UI builder to generate this
    """
    navbar_small_text: bool = Field(default=False, description="Small text on the top navbar")
    footer_small_text: bool = Field(default=False, description="Small text on the footer")
    body_small_text: bool = Field(default=False, description="Small text everywhere")
    brand_small_text: bool = Field(default=False, description="Small text on the brand/logo")
    brand_colour: Optional[str] = Field(default=None, description="Brand/logo background colour")
    accent: str = Field(default="accent-primary", description="Link colour")
    navbar: str = Field(default="navbar-white navbar-light", description="Topmenu colour")
    no_navbar_border: bool = Field(default=False, description="Topmenu border")
    navbar_fixed: bool = Field(
        default=False, description="Make the top navbar sticky, keeping it in view as you scroll"
    )
    layout_boxed: bool = Field(
        default=False, description="Whether to constrain the page to a box (leaving big margins at the side)"
    )
    actions_sticky_top: bool = Field(
        default=False, description="Make the actions bar sticky, keeping it in view as you scroll"
    )

    footer_fixed: bool = Field(default=False, description="Make the footer sticky, keeping it in view all the time")
    sidebar_fixed: bool = Field(default=False, description="Make the sidebar sticky, keeping it in view as you scroll")

    sidebar: str = Field(default="sidebar-dark-primary", description="Sidemenu colour")
    sidebar_nav_small_text: bool = Field(default=False, description="Sidemenu small text")
    sidebar_disable_expand: bool = Field(default=False, description="Disable expanding on hover of collapsed sidebar")
    sidebar_nav_child_indent: bool = Field(default=False, description="Indent child menu items on sidebar")
    sidebar_nav_compact_style: bool = Field(default=False, description="Use a compact sidebar")
    sidebar_nav_legacy_style: bool = Field(default=False, description="Use the AdminLTE2 style sidebar")
    sidebar_nav_flat_style: bool = Field(default=False, description="Use a flat style sidebar")

    theme: Theme = Field(default=Theme.default, description="Bootstrap theme to use (default, or from bootswatch)")
    dark_mode_theme: Optional[Theme] = Field(
        default=None, description="Theme to use instead if the user has opted for dark mode"
    )
    button_classes: ButtonClasses = Field(
        default_factory=ButtonClasses, description="The classes/styles to use with buttons"
    )

    def get_css_classes(self) -> ElementClasses:
        """
        Convert the UI tweaks into classes for the template
        """
        classes = ElementClasses(
            theme=self.theme,
            dark_mode_theme=self.dark_mode_theme,
            raw=self.model_dump(mode="json"),
            sidebar_classes=[
                self.sidebar,
                "sidebar-no-expand" if self.sidebar_disable_expand else "",
                "text-sm" if self.sidebar_nav_small_text else "",
            ],
            navbar_classes=[
                self.navbar,
                "text-sm" if self.navbar_small_text else "",
                "border-bottom-0" if self.no_navbar_border else "",
            ],
            body_classes=[
                self.accent,
                f"theme-{self.theme.value}",
                "dark-mode" if self.theme.is_dark() else "",
                "text-sm" if self.body_small_text else "",
                "layout-navbar-fixed" if self.navbar_fixed and not self.layout_boxed else "",
                "layout-footer-fixed" if self.footer_fixed and not self.layout_boxed else "",
                "layout-boxed" if self.layout_boxed else "",
            ],
            actions_classes=["sticky-top" if self.actions_sticky_top else ""],
            sidebar_list_classes=[
                "nav-child-indent" if self.sidebar_nav_child_indent else "",
                "nav-compact" if self.sidebar_nav_compact_style else "",
                "nav-legacy" if self.sidebar_nav_legacy_style else "",
                "nav-flat" if self.sidebar_nav_flat_style else "",
            ],
            brand_classes=[
                "text-sm" if self.brand_small_text else "",
                self.brand_colour or "",
            ],
            button_classes=self.button_classes,
            footer_classes=[
                "text-sm" if self.footer_small_text else ""
            ],
        )

        # Remove empty strings
        for key, value in classes.model_dump().items():
            if isinstance(value, list):
                setattr(classes, key, [x for x in value if x])

        return classes
