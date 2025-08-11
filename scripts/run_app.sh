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

hatch run aita -- --prompt "Find me Flights and Hotels to travel from Berlin to Sydney, area Bondi Beach, starting from 5th January, with a flexibility of 2 days, staying between 7 to 8 days, with Flights departing between 09:00 and 18:00, in a Hotel with 4 stars, within 200m from the beach."
echo

popd > /dev/null
