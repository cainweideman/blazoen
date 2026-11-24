import flet as ft
import flet_shadcn_ui as shad

from pages.home import HomePage

from services.settings import SettingsContext, laad_settings, bewaar_settings


@ft.component
def App():
    settings, set_settings = ft.use_state(laad_settings)

    def wijzig(**nieuw):
        def bijwerken(huidig):
            resultaat = huidig | nieuw
            bewaar_settings(resultaat)
            return resultaat
        set_settings(bijwerken)

    return SettingsContext(
        (settings, wijzig),
        lambda: ft.Router(
            routes=[
                ft.Route(index=True, component=HomePage)
            ],
            manage_views=True
        )
    )


def main(page: ft.Page) -> None:
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.render_views(component=App)
    page.window.icon = "blazoen.ico"
    page.theme = ft.Theme(use_material3=False)
    #page.window.frameless = True

ft.run(main, assets_dir="assets")
