#!/bin/bash

# This script formats the code using Black and lints it using Ruff.
# It uses a Hatch environment to ensure all dependencies are correctly installed.
# It can be used on CI/CD pipelines or locally.

SCRIPT_DIR=`dirname $0`
ROOT_DIR=$SCRIPT_DIR/..

pushd $ROOT_DIR > /dev/null

echo "🔎 Ensuring Hatch environment is created/updated with dependencies from pyproject.toml..."
hatch env create

echo
echo "🚀 Formatting..."

# Format all code
hatch run black .


echo
echo "🚀 Linting..."

# Automatically fix fixable Ruff issues
hatch run ruff check . --fix
echo

popd > /dev/null
