#! /usr/bin/env bash

set -euo pipefail

DEST_REPL="${HOME}/Library/ApplicationSupport/iTerm2/Scripts"
DEST_AL="${DEST_REPL}/AutoLaunch"

echo "copying files.."

mkdir -pv $DEST_AL
[[ ! -z $(ls -l src/REPL) ]] && cp -v src/REPL/*.py $DEST_REPL/
[[ ! -z $(ls -l src/AutoLaunch) ]] && cp -v src/AutoLaunch/*.py $DEST_AL/

echo "done"
