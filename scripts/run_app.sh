#!/bin/bash

SCRIPT_DIR=`dirname $0`
ROOT_DIR=$SCRIPT_DIR/..

pushd $ROOT_DIR > /dev/null

echo "🔎 Ensuring Hatch environment is created/updated with dependencies from pyproject.toml..."
hatch env create

echo
echo "🚀 Running aita..."

hatch run aita -- --version
echo

# hatch run aita -- --prompt "From Copenhagen to Rome staying between 5 to 10 days in July, looking for a 4 stars hotel in area Colosseum. All-Inclusive preferred."
# echo

popd > /dev/null
