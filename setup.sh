#!/bin/bash

if [ ! -d venv/ ]; then
  python -m venv venv
fi

if [[ $VIRTUAL_ENV != "" ]]; then
  deactivate
fi

source venv/bin/activate

pip install -r requirements.txt
