import flet as ft
import flet_shadcn_ui as shad

#from pathlib import Path

from models.models import Etiket
from components.zoekbalk import Zoekbalk

#from services.laad_blokken import laad_blokken


#BLOKKEN = laad_blokken(Path("/Users/cainweideman/Projects/flet-test/data/data.xlsx"))
# ---------------------------------------------------------------------------
# Losse invoervelden: krijgen hun waarde + een callback van de parent
# ---------------------------------------------------------------------------

def ReeksInvoer(van: str, tot: str, on_van, on_tot, error: str | None = None):
    return ft.Column(
        tight=True,
        controls=[
            ft.Row(
                controls=[
                    shad.Input(label="Van", placeholder="1", expand=True,
                               value=van, error_text=error,
                               on_change=lambda e: on_van(e.control.value)),
                    shad.Input(label="Tot en met", placeholder="optioneel", expand=True,
                               value=tot,
                               on_change=lambda e: on_tot(e.control.value)),
                ]
            ),
            ft.Text("Laat 'tot en met' leeg voor één etiket.", size=12, color="#737373"),
        ]
    )

def Kop(titel: str, sub: str):
    return ft.ListTile(
        dense=True,
        content_padding=0,
        title=ft.Text(titel, size=16, weight=ft.FontWeight.W_600),
        subtitle=ft.Text(sub, size=14, color="#737373"),
    )


def ToevoegKnop(on_click):
    return shad.Button(width=440, content="Toevoegen",
                       leading=shad.LucideIcons.PLUS, on_click=on_click)


MAX_REEKS = 500  # beveiliging tegen een typfout als 1 - 100000


def reeks_nummers(van: str, tot: str) -> tuple[list[str], str | None]:
    """Geeft (nummers, foutmelding) terug: één nummer per etiket."""
    van, tot = van.strip(), tot.strip()
    if not van:
        return [], "Vul het eerste getal in"
    if van and not van.isdigit():
        return [], "'Van' moet een getal zijn"
    if not tot:
        return [van], None
    if not tot.isdigit():
        return [], "'Tot en met' moet een getal zijn"
    if int(tot) < int(van):
        return [], "'Tot en met' moet groter zijn dan 'Van'"
    aantal = int(tot) - int(van) + 1
    if aantal > MAX_REEKS:
        return [], f"Maximaal {MAX_REEKS} etiketten per keer ({aantal} gevraagd)"
    return [str(n) for n in range(int(van), int(tot) + 1)], None

@ft.component
def Error(errors: dict):
    visible=True
    if errors.get("blok"):
        text = errors.get("blok", "")
    elif errors.get("reeks"):
        text = errors.get("reeks", "")
    elif errors.get("eigen"):
        text = errors.get("eigen", "")
    else:
        text = ""
        visible = False
    return ft.Row(
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        visible=visible,
        controls=[
            ft.Icon(icon=shad.LucideIcons.ALERT_CIRCLE, size=16, color=ft.Colors.ERROR),
            ft.Text(value=text, color=ft.Colors.ERROR, size=14)
        ]
    )


# ---------------------------------------------------------------------------
# Formulieren: hier zit de state van de velden
# ---------------------------------------------------------------------------

@ft.component
def StukkenForm(on_add, BLOKKEN):
    blok, set_blok = ft.use_state(None)
    modus, set_modus = ft.use_state("reeks")
    eigen_tekst, set_eigen_tekst = ft.use_state("")
    van, set_van = ft.use_state("")
    tot, set_tot = ft.use_state("")
    fout, set_fout = ft.use_state({})

    def toevoegen(_):
        if modus == "eigen":
            tekst = eigen_tekst.strip()
            teksten = [tekst] if tekst else []
            invoer_fout = None if tekst else "Vul een tekst in"
        else:
            teksten, invoer_fout = reeks_nummers(van, tot)
        fouten = {"blok": None if blok else "Kies een blok", modus: invoer_fout}
        set_fout(fouten)
        if any(fouten.values()):
            return
        on_add([Etiket("Stuk", blok, BLOKKEN[blok], t) for t in teksten])  # pyright: ignore[reportArgumentType]
        set_eigen_tekst("")
        set_van("")
        set_tot("")

    return ft.Column(
        tight=True,
        spacing=20,
        controls=[
            ft.Column(
                tight=True,
                spacing=8,
                controls=[
                    ft.Text("Blok", weight=ft.FontWeight.W_600),
                    Zoekbalk(BLOKKEN, set_blok)
                ]
            ),
            ft.Column(
                spacing=8,
                controls=[
                    ft.Text(value="Nummering", weight=ft.FontWeight.W_600),
                    ft.Container(
                        bgcolor="#FFFFFF",
                        padding=16,
                        border_radius=12,
                        border=ft.Border.all(width=1, color="#E4E4E7"),
                        content=shad.Tabs(
                            gap=20,
                            value=modus,
                            on_change=lambda e: set_modus(e.control.value),  # pyright: ignore[reportArgumentType]
                            tabs=[
                                shad.Tab(
                                    value="reeks",
                                    label="Reeks",
                                    content=ReeksInvoer(van, tot, set_van, set_tot),
                                ),
                                shad.Tab(
                                    value="eigen",
                                    label="Eigen tekst",
                                    content=ft.Column(
                                        tight=True,
                                        controls=[
                                            shad.Textarea(
                                                label="Tekst op het stuketiket",
                                                placeholder="Bijv.  1 - 24",
                                                value=eigen_tekst,
                                                #error_text=fout.get("eigen"),
                                                on_change=lambda e: set_eigen_tekst(e.control.value),
                                                description=ft.Text(value="Maximaal 1 regel.", size=12, color="#737373")
                                            )
                                        ]
                                    ),
                                )
                            ],
                        ),
                    ),
                ]
            ),
            Error(fout),
            ToevoegKnop(toevoegen),
        ],
    )
    

@ft.component
def DozenForm(on_add, BLOKKEN):
    blok, set_blok = ft.use_state(None)
    modus, set_modus = ft.use_state("reeks")
    eigen_tekst, set_eigen_tekst = ft.use_state("")
    van, set_van = ft.use_state("")
    tot, set_tot = ft.use_state("")
    formaat, set_formaat = ft.use_state("breed")
    fout, set_fout = ft.use_state({})

    def toevoegen(_):
        if modus == "eigen":
            tekst = eigen_tekst.strip()
            teksten = [tekst] if tekst else []
            invoer_fout = None if tekst else "Vul een tekst in"
        else:
            teksten, invoer_fout = reeks_nummers(van, tot)
        fouten = {"blok": None if blok else "Kies een blok", modus: invoer_fout}
        set_fout(fouten)
        if any(fouten.values()):
            return
        on_add([Etiket(soort="Doos", blok_nr=blok, blok=BLOKKEN[blok], tekst=t, formaat=formaat) for t in teksten])  # pyright: ignore[reportArgumentType]
        set_eigen_tekst("")
        set_van("")
        set_tot("")

    return ft.Column(
        tight=True,
        spacing=20,
        controls=[
            ft.Column(
                tight=True,
                spacing=8,
                controls=[
                    ft.Text("Blok", weight=ft.FontWeight.W_600),
                    Zoekbalk(BLOKKEN, set_blok)
                ]
            ),
            ft.Column(
                tight=True,
                spacing=8,
                controls=[
                    ft.Text("Formaat", weight=ft.FontWeight.W_600),
                    shad.Tabs(
                        value=formaat,
                        on_change=lambda e: set_formaat(e.control.value),  # pyright: ignore[reportArgumentType]
                        tabs=[
                            shad.Tab(
                                value="smal",
                                label="Smal",
                            ),
                            shad.Tab(
                                value="breed",
                                label="Breed",
                            ),
                        ],
                    ),
                ],
            ),
            ft.Column(
                spacing=8,
                controls=[
                    ft.Text(value="Nummering", weight=ft.FontWeight.W_600),
                    ft.Container(
                        bgcolor="#FFFFFF",
                        padding=16,
                        border_radius=12,
                        border=ft.Border.all(width=1, color="#E4E4E7"),
                        content=shad.Tabs(
                            gap=20,
                            value=modus,
                            on_change=lambda e: set_modus(e.control.value),  # pyright: ignore[reportArgumentType]
                            tabs=[
                                shad.Tab(
                                    value="reeks",
                                    label="Reeks",
                                    content=ReeksInvoer(van, tot, set_van, set_tot),
                                ),
                                shad.Tab(
                                    value="eigen",
                                    label="Eigen tekst",
                                    content=ft.Column(
                                        tight=True,
                                        controls=[
                                            shad.Textarea(
                                                label="Tekst op het doosetiket",
                                                placeholder="Bijv.  1 - 24",
                                                value=eigen_tekst,
                                                #error_text=fout.get("eigen"),
                                                on_change=lambda e: set_eigen_tekst(e.control.value),
                                                description=ft.Text(value="Maximaal 2 regels.", size=12, color="#737373")
                                            )
                                        ]
                                    ),
                                )
                            ],
                        ),
                    ),
                ]
            ),
            Error(fout),
            ToevoegKnop(toevoegen),
        ],
    )

def Header(modus: str):
    if modus == "stukken":
        title_text = "Nieuwe stuketiketten"
        subtitle_text = "Kies het blok en een reeks of eigen tekst. Elk stuketiket krijg één nummer."
    else:
        title_text = "Nieuwe doosetiketten"
        subtitle_text = "Kies het blok, het formaat en hoe de dozen genummerd worden."
    
    return ft.Container(
        content=ft.Column(
            spacing=6,
            controls=[
                ft.Text(value=title_text, size=28, weight=ft.FontWeight.W_600),
                ft.Text(value=subtitle_text, size=14, color="#666666")
            ]
        ) 
    )

@ft.component
def InputCard(on_add, BLOKKEN):
    tab, set_tab = ft.use_state("stukken")
    return ft.Container(
        width=440,
        padding=ft.Padding.symmetric(vertical=32, horizontal=28),
        content=ft.Column(
            spacing=24,
            controls=[
                Header(tab),
                shad.Tabs(
                    gap=24,
                    value=tab,
                    on_change=lambda e: set_tab(e.control.value),  # pyright: ignore[reportArgumentType]
                    tabs=[
                        shad.Tab(label="Stukken", value="stukken", content=StukkenForm(on_add=on_add, BLOKKEN=BLOKKEN)),
                        shad.Tab(label="Dozen", value="dozen", content=DozenForm(on_add=on_add, BLOKKEN=BLOKKEN)),
                    ]
                ),
            ]
        )
    )