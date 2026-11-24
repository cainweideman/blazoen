import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from models.models import Etiket

def open_html(html: str) -> None:
    data = html.encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    server = HTTPServer(("127.0.0.1", 0), Handler)  # poort 0 = vrije poort
    threading.Thread(target=server.handle_request, daemon=True).start()  # één request
    webbrowser.open(f"http://127.0.0.1:{server.server_port}/")


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