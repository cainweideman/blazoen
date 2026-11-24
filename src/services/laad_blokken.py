from openpyxl import Workbook, load_workbook
import flet as ft
import flet_shadcn_ui as shad

def laad_blokken(pad) -> dict:
    try:
        wb = load_workbook(pad, read_only=True, data_only=True)
        ws = wb.active
        blokken = {}
        for blok_nr, blok_naam, id, _ in ws.iter_rows(min_row=2, values_only=True):  # pyright: ignore[reportOptionalMemberAccess]
            if blok_nr is None:
                continue
            blokken[str(blok_nr).strip()] = str(blok_naam or "").strip()
        wb.close()
        ft.context.page.show_dialog(
            shad.Sonner(
                title="Blokken geladen",
                description=f"{len(blokken)} blokken"
            )
        )
        return blokken
    except Exception as e:
        ft.context.page.show_dialog(
            shad.Sonner(
                title="Kan blokken niet laden",
                description=str(e),
                variant=shad.ToastVariant.DESTRUCTIVE
            )
        )
        return {}