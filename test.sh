#!/bin/bash
set -e

if [ -f "venv/bin/activate" ]; then
  # Linux / macOS
  source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
  # Windows (Git Bash, Cygwin, or WSL)
  source venv/Scripts/activate
else
  echo "Error: Could not find Python virtual environment activation script."
  echo "Please create one with: python -m venv venv"
  exit 1
fi

python -m pytest $1/test_verify.py -s -vv
