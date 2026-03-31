#!/bin/bash

PYTHONPATH=. uv run python scripts/test-download.py "$1"
