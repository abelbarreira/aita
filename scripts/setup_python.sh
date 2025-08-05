#!/bin/bash

SCRIPT_DIR=`dirname $0`
ROOT_DIR=$SCRIPT_DIR/..

pushd $ROOT_DIR > /dev/null

pyenv install 3.13.3 # Install 3.13.3
pyenv local 3.13.3 # Use 3.13.3 in this shell

if python -m pip show pipx > /dev/null 2>&1; then
    # If pip is installed it upgrades it
    python -m pip install --upgrade --user pipx
else
    # If not, then it install it
    python -m pip install --user pipx
fi

python -m pipx ensurepath

popd > /dev/null
