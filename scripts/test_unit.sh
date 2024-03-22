#!/bin/bash
PYTHONPATH="controller/src/controller:." pytest controller/tests/
PYTHONPATH="gatekeeper/src/gatekeeper:." pytest gatekeeper/tests/
PYTHONPATH="trains/src/trains:." pytest trains/tests/
