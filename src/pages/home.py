from pathlib import Path

import flet as ft
import flet_shadcn_ui as shad

from components.navbar import NavBar
from components.input_card import InputCard
from components.etiket_tabel import EtiketTabel, Etiket

from services.html import open_html, bouw_html

from services.laad_blokken import laad_blokken

from services.settings import SettingsContext


@ft.component
def PadStuk():
    settings, wijzig = ft.use_context(SettingsContext)

    async def change_pad():
        new_pad = await ft.FilePicker().pick_files(allow_multiple=False)
        if new_pad:
            wijzig(stuk_pad=new_pad[0].path)
            ft.context.page.show_dialog(
                dialog=shad.Sonner(
                    title="Pad naar stuketiket sjabloon gewijzigd",
                    description=new_pad[0].path
                )
            )

    input = ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=shad.Input(
            disabled=True,
            value=settings.get("stuk_pad", ""),
            expand=True,
            height=40
        )
    )

    pad_exists = Path(settings.get("stuk_pad", "")).exists()

    exist_indicator = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        controls=[
            ft.Container(width=8, height=8, border_radius=999, bgcolor="#017A56" if pad_exists else ft.Colors.ERROR),
            ft.Text(value="Gevonden" if pad_exists else "Niet gevonden", size=12, style=ft.TextStyle(height=1), color="#017A56" if pad_exists else ft.Colors.ERROR)
        ]
    )

    return ft.Container(
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(value="Sjabloon stuketiket", weight=ft.FontWeight.W_500, style=ft.TextStyle(height=1)),
                        exist_indicator,
                    ]
                ),
                ft.Row(
                    controls=[
                        input,
                        shad.Button(
                            bgcolor="#FFFFFF",
                            content="Bladeren...",
                            variant=shad.ButtonVariant.OUTLINE,
                            height=40,
                            on_click=change_pad
                        )
                    ]
                ),
                ft.Text(value="HTML-bestand met de opmaak van een stuketiket.", size=12, color="#737373")
            ]
        )
    )

@ft.component
def DoosStuk():
    settings, wijzig = ft.use_context(SettingsContext)

    async def change_pad():
        new_pad = await ft.FilePicker().pick_files(allow_multiple=False)
        if new_pad:
            wijzig(doos_pad=new_pad[0].path)
            ft.context.page.show_dialog(
                dialog=shad.Sonner(
                    title="Pad naar doosetiket sjabloon gewijzigd",
                    description=new_pad[0].path
                )
            )

    input = ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=shad.Input(
            disabled=True,
            value=settings.get("doos_pad", ""),
            expand=True,
            height=40
        )
    )

    pad_exists = Path(settings.get("doos_pad", "")).exists()

    exist_indicator = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        controls=[
            ft.Container(width=8, height=8, border_radius=999, bgcolor="#017A56" if pad_exists else ft.Colors.ERROR),
            ft.Text(value="Gevonden" if pad_exists else "Niet gevonden", size=12, style=ft.TextStyle(height=1), color="#017A56" if pad_exists else ft.Colors.ERROR)
        ]
    )

    return ft.Container(
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(value="Sjabloon doosetiket", weight=ft.FontWeight.W_500, style=ft.TextStyle(height=1)),
                        exist_indicator,
                    ]
                ),
                ft.Row(
                    controls=[
                        input,
                        shad.Button(
                            bgcolor="#FFFFFF",
                            content="Bladeren...",
                            variant=shad.ButtonVariant.OUTLINE,
                            height=40,
                            on_click=change_pad
                        )
                    ]
                ),
                ft.Text(value="HTML-bestand met de opmaak van een doosetiket.", size=12, color="#737373")
            ]
        )
    )

@ft.component
def BlokInput():
    settings, wijzig = ft.use_context(SettingsContext)

    async def change_pad():
        new_pad = await ft.FilePicker().pick_files(allow_multiple=False)
        if new_pad:
            wijzig(blok_pad=new_pad[0].path)

    input = ft.Container(
        expand=True,
        bgcolor="#FFFFFF",
        content=shad.Input(
            disabled=True,
            value=settings.get("blok_pad", ""),
            expand=True,
            height=40,
        )
    )

    pad_exists = Path(settings.get("blok_pad", "")).exists()

    exist_indicator = ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        controls=[
            ft.Container(width=8, height=8, border_radius=999, bgcolor="#017A56" if pad_exists else ft.Colors.ERROR),
            ft.Text(value="Gevonden" if pad_exists else "Niet gevonden", size=12, style=ft.TextStyle(height=1), color="#017A56" if pad_exists else ft.Colors.ERROR)
        ]
    )

    return ft.Container(
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(value="Excel-bestand met blokken", weight=ft.FontWeight.W_500, style=ft.TextStyle(height=1)),
                        exist_indicator,
                    ]
                ),
                ft.Row(
                    controls=[
                        input,
                        shad.Button(
                            bgcolor="#FFFFFF",
                            content="Bladeren...",
                            variant=shad.ButtonVariant.OUTLINE,
                            height=40,
                            on_click=change_pad
                        )
                    ]
                ),
                ft.Text(value="Kolom A: bloknummer, kolom B: naam", size=12, color="#737373")
            ]
        )
    )


@ft.component
def HomePage() -> ft.View:
    settings, wijzig = ft.use_context(SettingsContext)
    herlaad, set_herlaad = ft.use_state(0)
    blok_pad = settings.get("blok_pad", "")
    blokken = ft.use_memo(lambda: laad_blokken(blok_pad), [blok_pad, herlaad])
    etiketten, set_etiketten = ft.use_state([])
    soort = etiketten[0].soort if etiketten else None

    def opnieuw_inlezen():
        set_herlaad(lambda n: n + 1)

    def voeg_toe(nieuwe: list[Etiket]):
        def toevoegen(huidige):
            if huidige and nieuwe and nieuwe[0].soort != huidige[0].soort:
                ft.context.page.show_dialog(
                    shad.Toast(
                        title="Soorten kunnen niet gemengd worden",
                        description=f"De lijst bevat al etiketten voor {soort}. Verwijder deze eerst.",
                        variant=shad.ToastVariant.DESTRUCTIVE
                    )
                )
                return huidige
            return [*huidige, *nieuwe]
        set_etiketten(toevoegen)
    
    def verwijder(etiket: Etiket):
        set_etiketten(lambda huidige: [x for x in huidige if x.id != etiket.id])

    def alles_wissen():
        set_etiketten([])
    
    def verplaats(oud: int, nieuw: int):
        def herorden(huidige):
            lijst = list(huidige)
            lijst.insert(nieuw, lijst.pop(oud))
            return lijst
        set_etiketten(herorden)
    
    def naar_html():
        if not etiketten:
            ft.context.page.show_dialog(
                shad.Toast(
                    title="Niets om te openen",
                    description="Voeg eerst een etiket toe.",
                    variant=shad.ToastVariant.DESTRUCTIVE
                )
            )
            return
        
        try:
            if etiketten[0].soort == "Stuk":
                sjabloon = Path(settings.get("stuk_pad", ""))
            else:
                sjabloon = Path(settings.get("doos_pad", ""))
            html = bouw_html(etiketten, sjabloon_pad=sjabloon)
            open_html(html=html)
        except Exception as e:
            ft.context.page.show_dialog(
                shad.Sonner(
                    title="Etiketten kunnen niet worden gemaakt",
                    description=str(e),
                    variant=shad.ToastVariant.DESTRUCTIVE,
                )
            )

    actions=[
        ft.Row(
            spacing=10,
            controls=[
                shad.Button(
                    variant=shad.ButtonVariant.GHOST,
                    content="Alles wissen",
                    height=36,
                    on_click=lambda _: alles_wissen()
                ),
                shad.Button(
                    variant=shad.ButtonVariant.PRIMARY,
                    leading=shad.LucideIcons.EXTERNAL_LINK,
                    content="Openen in browser",
                    height=36,
                    on_click=lambda _: naar_html()
                ),
                ft.Container(height=24, width=1, bgcolor="#E4E4E7"),
                shad.IconButton(
                    icon=shad.LucideIcons.SETTINGS,
                    variant=shad.ButtonVariant.GHOST,
                    on_click=ft.context.page.show_end_drawer
                )
            ]
        )
    ]

    return ft.View(
        bgcolor="#fafafa",
        end_drawer=ft.NavigationDrawer(
            bgcolor="#FFFFFF",
            width=460,
            controls=[
                ft.Container(
                    border=ft.Border.only(bottom=ft.BorderSide(width=1, color="#E4E4E7")),
                    padding=ft.Padding.only(left=24, right=16),
                    height=76,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Instellingen", size=18, weight=ft.FontWeight.W_600),
                            shad.IconButton(
                                icon=shad.LucideIcons.X,
                                variant=shad.ButtonVariant.GHOST,
                                on_click=ft.context.page.close_end_drawer
                            )
                        ]
                    )
                ),
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=24, vertical=20),
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    spacing=14,
                                    controls=[
                                        ft.Text(value="Sjablonen", size=16, weight=ft.FontWeight.W_600, color="#737373"),
                                        PadStuk(),
                                        ft.Container(height=1),
                                        DoosStuk()
                                    ]
                                )
                            ),
                            ft.Container(
                                height=1,
                                expand=True,
                                bgcolor="#E4E4E7",
                                margin=ft.Margin.symmetric(vertical=24)
                            ),
                            ft.Container(
                                content=ft.Column(
                                    spacing=14,
                                    controls=[
                                        ft.Text(value="Blokken", size=16, weight=ft.FontWeight.W_600, color="#737373"),
                                        BlokInput(),
                                        ft.Container(
                                            padding=ft.Padding.symmetric(vertical=10, horizontal=12),
                                            border_radius=10,
                                            bgcolor="#F6F6F6",
                                            content=ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text(f"{len(blokken)} blokken ingelezen"),
                                                    shad.Button(
                                                        content="Opnieuw inlezen",
                                                        leading=shad.LucideIcons.ROTATE_CW,
                                                        variant=shad.ButtonVariant.OUTLINE,
                                                        bgcolor="#FFFFFF",
                                                        height=40,
                                                        on_click=lambda _: opnieuw_inlezen(),
                                                    )
                                                ]
                                            )
                                        )
                                    ]
                                )
                            ),
                        ]
                    )
                )
            ]
        ),
        padding=0,
        appbar=NavBar(actions=actions),
        controls=[
            ft.Container(
                expand=True,
                border=ft.Border.only(top=ft.BorderSide(width=1, color="#E4E4E7")),
                content=ft.Container(
                    expand=True,
                    content=ft.Row(
                        expand=True,
                        controls=[
                            InputCard(on_add=voeg_toe, BLOKKEN=blokken),
                            ft.Container(width=1, bgcolor="#E4E4E7"),
                            EtiketTabel(etiketten, on_delete=verwijder, on_move=verplaats)
                        ]
                    )
                )
            ),
        ]
    )