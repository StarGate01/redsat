#!/bin/bash

source /app/config/station.config

if [ -z "$1" ]; then
    SAT="MOVEII"
    echo "Warning: No satellite specified, defaulting to MOVE-II"
else
    SAT=$1
fi

# if [ -z "$2" ]; then
#     echo "Error: No input specified, aborting"
#     exit 1
# else
#     INPUT_BASE=$2
# fi

# OUTPUT=${INPUT_BASE}_$(date +%s)
# mkdir -p /app/output/$KIND/$OUTPUT

if [ "$SAT" == "MOVEII" ]; then
    echo "Starting MOVE-II fake server (local blackhole)"
    python /app/fakeserver/server.py &
fi

gnuradio-companion

# META_INFO=`cat /app/input/$INPUT_BASE.meta | paste -sd';'`

# python /app/gr/$KIND/decode.py --meta-input-file=/app/input/$INPUT_BASE.raw --meta-output-dir=/app/output/$KIND/$OUTPUT/ --meta-info=$META_INFO > /app/output/$KIND/$OUTPUT/decode.log