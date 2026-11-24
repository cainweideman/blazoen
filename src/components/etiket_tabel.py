import flet as ft
import flet_shadcn_ui as shad

from models.models import Etiket

def Header(etiketten: list[Etiket]):
    return ft.Container(
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(value="Gemaakte etiketten", size=28, weight=ft.FontWeight.W_600),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            value="Eén soort per lijst. Open in de browser om af te drukken.",
                            size=14,
                            color="#666666"
                        ),
                        ft.Container(
                            content=ft.Text(value=f"{len(etiketten)} etiketten", size=13),
                            bgcolor="#EFEFEF",
                            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                            border_radius=7
                        )
                    ]
                )
            ]
        )
    )

def EtiketTabel(etiketten: list[Etiket], on_delete=None, on_move=None):
    listview = ft.ListView(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=1,
        divider_thickness=1,
        controls=[
            ft.Container(
                content=ft.ListTile(
                    key=e.id,
                    leading=shad.IconButton(icon=ft.Icons.INVENTORY) if e.soort == "Doos" else shad.IconButton(icon=ft.Icons.INSERT_DRIVE_FILE_OUTLINED, variant=shad.ButtonVariant.OUTLINE,),
                    title=ft.Row(
                        spacing=4,
                        controls=[
                            ft.Text(
                                value=f"{e.blok_nr} ", 
                                style=ft.TextStyle(size=14, weight=ft.FontWeight.W_600)
                            ),
                            ft.Text(
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                value=f"{e.blok_naam} ", 
                                style=ft.TextStyle(size=14),
                                expand=True,
                            ),
                            shad.Badge(content="Smal") if e.soort == "Doos" and e.formaat == "smal" else ft.Text("")
                        ]
                    ),
                    subtitle=ft.Text(e.tekst),
                    trailing=shad.IconButton(
                        icon=shad.LucideIcons.TRASH,
                        variant=shad.ButtonVariant.GHOST,
                        on_click=lambda _, e=e: on_delete and on_delete(e)
                    )
                )
            )
            for e in etiketten
        ]
    )

    leeg = ft.Container(
        padding=ft.Padding.symmetric(vertical=40, horizontal=32),
        border_radius=12,
        bgcolor="#FFFFFF",
        border=ft.Border.all(width=1, color="#E4E4E7"),
        content=ft.Row(
            expand=True,
            spacing=24,
            controls=[
                ft.Image(src="blazoen-stapel-etiketten.svg", width=88, height=88),
                ft.Column(
                    expand=True,
                    spacing=6,
                    controls=[
                        ft.Text(value="Nog geen etiketten", weight=ft.FontWeight.W_600, size=15),
                        ft.Text(
                            value="Kies links stukken of dozen, het blok en de nummers. Wat je toevoegt verschijnt hier.",
                            color="#666666",
                            expand=True
                        ),
                    ]
                )
            ]
        )
    )

    return ft.Container(
        padding=ft.Padding.symmetric(vertical=32, horizontal=28),
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=20,
            controls=[
                Header(etiketten),
                leeg if not etiketten else ft.Container(expand=True, content=listview, border=ft.Border.all(width=1, color="#E4E4E7"), border_radius=12, bgcolor="#FFFFFF")
            ]
        )
    )

