#!/bin/bash

# This script creates or updates .vscode/settings.json with the "python.defaultInterpreterPath"
# pointing to the current Hatch environment's Python interpreter.
# This ensures VS Code uses the correct environment for linting, intellisense, and navigation.

SCRIPT_DIR=`dirname $0`
ROOT_DIR=$SCRIPT_DIR/..

pushd $ROOT_DIR > /dev/null

echo "🔎 Ensuring Hatch environment is created/updated with dependencies from pyproject.toml..."
hatch env create

echo
echo "🚀 Generating VSCode Settings.."

hatch run set-vscode-interpreter
echo

popd > /dev/null
