from __future__ import annotations
from enum import Enum
from typing import Optional


class Station(str, Enum):
    ADAMOWO = "Adamowo"
    BABIAK = "Babiak"
    CACKI = "Cacki"
    DALEKIE = "Dalekie"
    EMANUEL = "Emanuel"
    FALBANKA = "Falbanka"
    GADLIN = "Gadlin"
    HAJDUKI = "Hajduki"
    IGLICE = "Iglice"
    JACINKI = "Jacinki"
    KACZANOWO = "Kaczanowo"
    LAS = "Las"
    MA = "Ma"
    NADOLICE = "Nadolice"
    OBORA = "Obora"
    PABIANICE = "Pabianice"
    RACIBORY = "Racibory"
    SADKI = "Sadki"
    TANIECZNICA = "Taniecznica"
    UBLIK = "Ublik"

    @property
    def id(self) -> int:
        return list(Station.__members__).index(self.name)

    @classmethod
    def get_by_id(cls, id_: int) -> Optional[Station]:
        try:
            return list(cls.__members__.items())[id_][1]
        except IndexError:
            return None
