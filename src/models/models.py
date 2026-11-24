from dataclasses import dataclass, field
from itertools import count

_ids = count(1)

@dataclass
class Etiket:
    soort: str
    blok_nr: str
    blok: str
    tekst: str
    id: int = field(default_factory=lambda: next(_ids))
    formaat: str = field(default="breed")

    @property
    def blok_naam(self):
        return self.blok.replace(f"{self.blok_nr}.", "").strip()