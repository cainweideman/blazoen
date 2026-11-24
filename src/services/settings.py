import json
from pathlib import Path

import flet as ft

SETTINGS_PAD = Path(__file__).resolve().parent.parent / "assets" / "config.json"

def laad_settings(pad: Path = SETTINGS_PAD):
    with pad.open(encoding="utf-8") as f:
        return json.load(f)
    

def bewaar_settings(settings: dict) -> None:
    #GEBRUIKER_PAD.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PAD.write_text(json.dumps(settings, indent=2, ensure_ascii=False),
                             encoding="utf-8")

SettingsContext = ft.create_context(({}, lambda **_: None))