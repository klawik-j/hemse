#!/bin/bash

set -e

pip-compile pyproject.toml
pip-compile requirements-dev.in
