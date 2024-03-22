from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import relationship, selectinload, mapped_column, Mapped

from common.db import BaseModel
from common.station import Station
from models.gate_switch import GateSwitch
from settings import settings


class Gate(BaseModel):
    """
    Gate holds the state of each train station.

    Closes when a train is passing and opens otherwise.
    """

    __tablename__ = "gate"

    id: Mapped[int] = mapped_column(primary_key=True)
    closed: Mapped[bool] = mapped_column(nullable=False)
    open_permission: Mapped[str] = mapped_column(
        nullable=False,
        comment="only the last train to close the gate has the right to open it",
    )

    switches = relationship(
        "GateSwitch", back_populates="gate", order_by="desc(GateSwitch.created_at)"
    )

    @classmethod
    def get(cls, id_: int) -> Optional[Gate]:
        """Get `Gate` by id, with last related object included."""

        return (
            settings.db_session.query(Gate)
            .filter_by(id=id_)
            .options(selectinload(Gate.switches))
            .limit(1)
            .first()
        )

    @classmethod
    def get_for_update(cls, id_: int) -> Optional[Gate]:
        """
        Get `Gate` by id, with last related object included.

        The row is locked until committed to avoid concurrent updates.
        """

        return (
            settings.db_session.query(Gate)
            .filter_by(id=id_)
            .options(selectinload(Gate.switches))
            .limit(1)
            .with_for_update()
            .first()
        )

    def create(self) -> Gate:
        """
        Create new gate and immediately the related value change.

        :raises ValueError: if station is unknown for which a gate is attempted
        """

        if Station.get_by_id(self.id) is None:
            raise ValueError("Station unknown")

        self._save()

        return self

    def update(self, closed: bool, train_id: str) -> Gate:
        """Update gates state and create a related switch object."""

        self.closed = closed
        self.open_permission = train_id
        self._save()

        return self

    def _save(self) -> None:
        """Commit added to session changes."""

        settings.db_session.add(self)
        settings.db_session.add(GateSwitch(gate_id=self.id, value=self.closed))

        settings.db_session.commit()
        settings.db_session.close()
