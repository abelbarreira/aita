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

hatch run aita -- --prompt "Find me flights from Copenhagen to Tokyo in September..."
echo

popd > /dev/null
