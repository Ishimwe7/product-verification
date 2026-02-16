#!/bin/bash
echo "Running Unit and Integration Tests..."
export PYTHONPATH=.
python.exe -m pytest -v tests/