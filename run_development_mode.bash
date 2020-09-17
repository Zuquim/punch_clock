#!/usr/bin/env bash

# Exporting required environment variables
export FLASK_APP=punch_clock.py
export FLASK_ENV=development

# Making required local directories for development mode run
if [ ! -d log ]
then
  mkdir log
fi

# Checking environment Python version
PY_VER=$(python3 --version | awk '{print $2}')
if (( $(echo $PY_VER | sed -n 's/\.//gp') < 370 ))
then
  printf "\nError!\nMinimum Python version required:        3.7.0"
  printf "\nVersion running on current environment: {$PY_VER}\n"
  exit 1
fi

# Creating, activating and preparing local Python3 virtual environment to run
if [ ! -d venv ]
then
  python3 -m venv venv
fi
source venv/bin/activate
pip3 install -U pip setuptools
pip3 install -r requirements.txt

# Running Flask project in development mode
flask run --host=0.0.0.0 --port=5000 --with-threads
