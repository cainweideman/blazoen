import flet as ft
import flet_shadcn_ui as shad

async def show_sheet():
    sheet = shad.Sheet(
        title="Test",
        side=shad.SheetSide.LEFT,
        actions=[
            shad.Button("Test")
        ],
    )

    ft.context.page.show_dialog(sheet)

@ft.component
def NavBar(actions=None) -> ft.AppBar:
    return ft.AppBar(
        toolbar_height=76,
        elevation_on_scroll=0,
        elevation=0,
        bgcolor="#FFFFFF",
        automatically_imply_leading=False,
        title_spacing=28,
        title=ft.Container(
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Image(src="gra_beeldmerk.svg", height=32),
                    ft.Container(height=24, width=1, bgcolor="#E4E4E7"),
                    ft.Text(
                        value="Blazoen",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color='black'
                    ),
                ]
            ),
        ),
        center_title=False,
        actions=actions,
        actions_padding=ft.Padding.only(right=28)
    )