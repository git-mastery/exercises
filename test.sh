#!/bin/bash
set -e

uv run pytest "$1/test_verify.py" -s -vv
