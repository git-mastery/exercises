#!/bin/bash

if [ ! -d venv/ ]; then
  python -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt -U --no-cache-dir

if ! command -v lefthook &>/dev/null; then
  lefthook install
fi
