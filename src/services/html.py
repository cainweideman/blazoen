import atexit
import shutil
import tempfile
import webbrowser
from pathlib import Path

from models.models import Etiket

# Eén tijdelijke map voor alle geopende HTML-bestanden; weg bij afsluiten van de app.
TEMP_MAP = Path(tempfile.mkdtemp(prefix="blazoen_"))
atexit.register(shutil.rmtree, TEMP_MAP, ignore_errors=True)


def open_html(html: str) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=TEMP_MAP, delete=False, encoding="utf-8") as f:
        f.write(html)
    webbrowser.open_new_tab(Path(f.name).as_uri())


def bouw_html(etiketten: list[Etiket], sjabloon_pad: Path) -> str:
    #if etiketten[0].soort == "Stuk":
        #html = stuk_pad.read_text(encoding="utf-8")
    #else:
        #html = doos_pad.read_text(encoding="utf-8")
    html = sjabloon_pad.read_text(encoding="utf-8")
    labels = [
            f'''
            <div class="label {e.formaat}">
            <div class="blok_nummer">{e.blok_nr}</div>
            <div class="naam">{e.blok_naam}</div>
            <div class="doos_nummer">{e.tekst.replace("\n", "<br>")}</div>
            <div class="logo {e.formaat}">Groninger Archieven</div>
            </div>
            ''' for e in etiketten
    ]
    
    html = html.replace("<!-- LABELS_GO_HERE -->", (''.join(labels)))
    return html