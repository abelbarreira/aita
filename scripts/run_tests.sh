#!/bin/bash

SCRIPT_DIR=`dirname $0`
ROOT_DIR=$SCRIPT_DIR/..

pushd $ROOT_DIR > /dev/null

echo "🧹 Cleaning previous test reports..."
rm -rf test/reports/

echo "🔎 Ensuring Hatch environment is created/updated with dependencies from pyproject.toml..."
hatch env create

echo
echo "🚀 Testing aita..."

hatch run test
echo

popd > /dev/null