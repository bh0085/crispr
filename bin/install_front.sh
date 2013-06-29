#!/usr/bin/env bash
# installs virtualenv and development.ini

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../frontend
virtualenv venv
cfront 
pip install pyramid
python setup.py develop


