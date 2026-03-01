#!/bin/bash

if [ ! -d venv/ ]; then
  python -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt -U --no-cache-dir

if command -v lefthook  >/dev/null 2>&1; then
  lefthook install
else
  echo "LeftHook not installed, failed to set up LeftHook for Git Hooks."
fi
