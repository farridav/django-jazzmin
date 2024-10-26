from enum import StrEnum


class ChangeFormTemplate(StrEnum):
    single = "single"
    carousel = "carousel"
    collapsible = "collapsible"
    horizontal_tabs = "horizontal_tabs"
    vertical_tabs = "vertical_tabs"

    @staticmethod
    def get_template(choice: "ChangeFormTemplate") -> str:
        return f"jazzmin/includes/{choice.name}.html"


class DarkThemes(StrEnum):
    darkly = "darkly"
    cyborg = "cyborg"
    slate = "slate"
    solar = "solar"
    superhero = "superhero"


class Themes(StrEnum):
    # light themes
    default = "vendor/bootswatch/default/bootstrap.min.css"
    cerulean = "vendor/bootswatch/cerulean/bootstrap.min.css"
    cosmo = "vendor/bootswatch/cosmo/bootstrap.min.css"
    flatly = "vendor/bootswatch/flatly/bootstrap.min.css"
    journal = "vendor/bootswatch/journal/bootstrap.min.css"
    litera = "vendor/bootswatch/litera/bootstrap.min.css"
    lumen = "vendor/bootswatch/lumen/bootstrap.min.css"
    lux = "vendor/bootswatch/lux/bootstrap.min.css"
    materia = "vendor/bootswatch/materia/bootstrap.min.css"
    minty = "vendor/bootswatch/minty/bootstrap.min.css"
    pulse = "vendor/bootswatch/pulse/bootstrap.min.css"
    sandstone = "vendor/bootswatch/sandstone/bootstrap.min.css"
    simplex = "vendor/bootswatch/simplex/bootstrap.min.css"
    sketchy = "vendor/bootswatch/sketchy/bootstrap.min.css"
    spacelab = "vendor/bootswatch/spacelab/bootstrap.min.css"
    united = "vendor/bootswatch/united/bootstrap.min.css"
    yeti = "vendor/bootswatch/yeti/bootstrap.min.css"
    darkly = "vendor/bootswatch/darkly/bootstrap.min.css"
    cyborg = "vendor/bootswatch/cyborg/bootstrap.min.css"
    slate = "vendor/bootswatch/slate/bootstrap.min.css"
    solar = "vendor/bootswatch/solar/bootstrap.min.css"
    superhero = "vendor/bootswatch/superhero/bootstrap.min.css"

    def is_dark(self) -> bool:
        return self in DarkThemes.__members__.values()
