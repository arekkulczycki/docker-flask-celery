#!/bin/bash
pyright .
black --check .
flake8 common --config=common/.flake8
flake8 controller --config=controller/.flake8
flake8 gatekeeper --config=gatekeeper/.flake8
flake8 trains --config=trains/.flake8
