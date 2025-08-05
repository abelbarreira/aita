#!/bin/bash

SCRIPT_DIR=`dirname $0`
ROOT_DIR=$SCRIPT_DIR/..
APP_DIR=$ROOT_DIR/app

pushd $APP_DIR > /dev/null

export PYTHONPATH=$(pwd) # So aita is found when Python resolves imports

echo
echo "Running ./aita/main.py --version"
./aita/main.py --version # direct script call

echo
echo "Running python ./app/main.py --version"
python ./aita/main.py --version # explicit interpreter call

echo
echo "Running python -m aita.main --version"
python -m aita.main --version # module execution

popd > /dev/null
