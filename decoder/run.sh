#!/bin/bash

source /app/TLE/station.config

if [ -z "$1" ]; then
    SAT="move2"
    echo "Warning: No kind specified, defaulting to move2"
else
    SAT=$1
fi

if [ -z "$2" ]; then
    echo "Error: No input specified, aborting"
    exit 1
else
    INPUT_BASE=$2
fi

OUTPUT=${INPUT_BASE}_$(date +%s)
mkdir -p /app/output/$KIND/$OUTPUT

META_INFO=`cat /app/input/$INPUT_BASE.meta | paste -sd';'`

python /app/gr/$KIND.py --meta-input-file=/app/input/$INPUT_BASE.raw --meta-output-dir=/app/output/$KIND/$OUTPUT/ --meta-info=$META_INFO > /app/output/$KIND/$OUTPUT/decode.log