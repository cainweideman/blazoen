import flet as ft
import flet_shadcn_ui as shad


MAX = 50

def filter_blokken(items: dict[str, str], query: str) -> list[tuple[str, str]]:
    q = query.strip().lower()
    if not q:
        return list(items.items())[:MAX]
    hits = []
    for nr, naam in items.items():
        if nr.lower().startswith(q) or q in naam.lower():
            hits.append((nr, naam))
            if len(hits) == MAX:
                break
    return hits


@ft.component
def Zoekbalk(items: dict[str, str], on_kies):
    query, set_query = ft.use_state("")
    hits = ft.use_memo(lambda: filter_blokken(items, query), [query])

    async def kies(e: ft.Event[ft.ListTile]):
        nr, naam = e.control.key, e.control.data
        tekst = f"{nr} - {naam}"
        set_query(tekst)
        on_kies(nr)
        await anchor.close_view(tekst)
    
    async def handle_tap(e: ft.Event[ft.SearchBar]):
        await anchor.open_view()
    
    async def handle_delete(e):
        set_query("")
        on_kies(None)

    anchor = ft.SearchBar(
        height=40,
        view_header_height=40,
        value=query,
        bar_hint_text="Zoek op nummer of naam",
        bar_leading=ft.Icon(ft.Icons.SEARCH, size=18, color="#71717A"),
        view_leading=ft.Icon(icon=ft.Icons.SEARCH, size=18, color="#71717A"),
        bar_trailing=shad.IconButton(  # pyright: ignore[reportArgumentType]
            icon=shad.LucideIcons.X,
            variant=shad.ButtonVariant.GHOST,
            on_click=handle_delete
        ),
        view_trailing=shad.IconButton(  # pyright: ignore[reportArgumentType]
            icon=shad.LucideIcons.X,
            variant=shad.ButtonVariant.GHOST,
            on_click=handle_delete
        ),
        bar_shape=ft.RoundedRectangleBorder(side=ft.BorderSide(1, color="#E4E4E7"), radius=8),
        bar_bgcolor="#FFFFFF",
        bar_overlay_color="#FFFFFF",
        view_bgcolor="#FFFFFF",
        view_shape=ft.RoundedRectangleBorder(side=ft.BorderSide(1, color="#E4E4E7"), radius=8),
        divider_color="#E4E4E7",
        bar_elevation=0,
        view_elevation=0,
        shrink_wrap=True,
        on_change=lambda e: set_query(e.control.value),
        on_tap=handle_tap,
        controls=[
            ft.ListTile(
                key=nr,
                data=naam,
                dense=True,
                leading=ft.Text(nr, size=13, color="#71717A"),
                title=ft.Text(naam, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                on_click=kies
            )
            for nr, naam in hits
        ],
    )
    return anchor