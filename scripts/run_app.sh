#!/bin/bash

SCRIPT_DIR=`dirname $0`
ROOT_DIR=$SCRIPT_DIR/..

pushd $ROOT_DIR > /dev/null

# echo
# echo "🚀 Running hatch env prune"
# hatch env prune

echo
echo "🚀 Running hatch run python -m aita.main --version"
hatch run python -m aita.main --version

echo
echo "🚀 Running hatch run aita -- --version"
hatch run aita -- --version

# Or directly in the terminal with Interactive Shell:
# hatch shell
# aita --version
# exit

popd > /dev/null
