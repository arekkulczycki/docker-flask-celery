from datetime import datetime
from logging import getLogger
from typing import Optional, Tuple

from flask import Blueprint
from flask_pydantic import validate
from pydantic import BaseModel

from models.gate import Gate
from views.error_response import ErrorResponse
from views.gate_status_response import GateStatusResponse

route_blueprint = Blueprint(
    "route",
    __name__,
)
logger = getLogger("app")


@route_blueprint.route("/gate/<gate_id>", methods=["GET"])
@validate()
def get_gate_status(gate_id: int) -> Tuple[BaseModel, int]:
    """Get state of the gate and the last datetime it was switched."""

    gate: Optional[Gate] = Gate.get(gate_id)

    if gate is None:
        return ErrorResponse(error="Not found"), 400

    logger.info(f"gate {gate_id} status: {gate.closed}")

    return (
        GateStatusResponse(
            closed=gate.closed,
            last_change=gate.switches[0].created_at,
            train_id=gate.open_permission,
        ),
        200,
    )


class ToggleGateBody(BaseModel):
    train_id: str


@route_blueprint.route("/gate/<gate_id>/<state>", methods=["PUT"])
@validate()
def toggle_gate(
    gate_id: int, state: int, form: ToggleGateBody
) -> Tuple[BaseModel, int]:
    """
    Change state of the gate or create a new object if did not exist.

    Queried gate is locked until committed to avoid concurrent updates.
    """

    logger.info(f"setting gate {gate_id} to {state}")
    try:
        gate: Optional[Gate] = Gate.get_for_update(gate_id)
    except Exception as e:
        logger.error(e)
        raise

    if gate is None:
        gate = _try_create_gate(gate_id, state, form.train_id)
    else:
        gate.update(bool(state), form.train_id)

    if gate is None:
        return ErrorResponse(error="Not found"), 400

    return (
        GateStatusResponse(
            closed=gate.closed, last_change=datetime.now(), train_id=form.train_id
        ),
        200,
    )


def _try_create_gate(gate_id, state, train_id) -> Optional[Gate]:
    try:
        return Gate(id=gate_id, closed=bool(state), open_permission=train_id).create()
    except ValueError:
        return None
