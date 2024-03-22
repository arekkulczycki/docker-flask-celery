from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from common.db import BaseModel

if TYPE_CHECKING:
    from models.gate import Gate


class GateSwitch(BaseModel):
    """
    Historical record of a change in a gate.
    """

    __tablename__ = "gate_switch"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gate_id: Mapped[int] = mapped_column(ForeignKey("gate.id"), nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    gate: Mapped[Gate] = relationship("Gate", back_populates="switches")
