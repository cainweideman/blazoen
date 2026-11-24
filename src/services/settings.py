import json
import os
import sys
from pathlib import Path

import flet as ft

# Standaardinstellingen die met de app worden meegeleverd (alleen lezen).
STANDAARD_PAD = Path(__file__).resolve().parent.parent / "assets" / "config.json"

# Instellingen van de gebruiker: blijven bewaard, ook in een gebouwde .exe.
if sys.platform == "win32":
    GEBRUIKER_PAD = Path(os.environ["APPDATA"]) / "Blazoen" / "config.json"
else:
    GEBRUIKER_PAD = Path.home() / "Library" / "Application Support" / "Blazoen" / "config.json"


def laad_settings():
    pad = GEBRUIKER_PAD if GEBRUIKER_PAD.exists() else STANDAARD_PAD
    return json.loads(pad.read_text(encoding="utf-8"))


def bewaar_settings(settings: dict) -> None:
    GEBRUIKER_PAD.parent.mkdir(parents=True, exist_ok=True)
    GEBRUIKER_PAD.write_text(json.dumps(settings, indent=2, ensure_ascii=False),
                             encoding="utf-8")

SettingsContext = ft.create_context(({}, lambda **_: None))
