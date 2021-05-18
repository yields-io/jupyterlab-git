#!/bin/bash

set -e
rm -rf dist
pip install build twine
python -m build --wheel
twine upload --repository-url https://nexus.yields.io/repository/y-python-release/ dist/*
