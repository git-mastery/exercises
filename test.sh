#!/bin/bash

source venv/bin/activate

python -m pytest $1/tests/test_verify.py -s -vv
