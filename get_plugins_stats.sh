#!/bin/bash


function main {
    local CURR_DIR=$(dirname $0)
    export PYTHONPATH="$CURR_DIR/venv/lib/python3.6/site-packages"

	python3 "$CURR_DIR/src/main.py" "$CURR_DIR/conf/user.conf"

}

set -x;

main "$@"
