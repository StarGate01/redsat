#!/bin/bash

: "${REDSAT_CONFIG_DIR:=/app/config}"
: "${REDSAT_INPUT_DIR:=/app/input}"

source ${REDSAT_CONFIG_DIR}/station.config

if [ -z "$1" ]; then
    SAT="MOVEII"
    echo "Warning: No satellite specified, defaulting to MOVE-II"
else
    SAT=$1
fi

if [ -z "$2" ]; then
    echo "Warning: No input file specified"
    exit 1
else
    INPUT=$2
fi

if [ -z "$3" ]; then
    echo "Warning: No output time stamp specified"
    exit 1
else
    OUTPUT_BASE=$3
fi

FREQ=`grep "$SAT" "$REDSAT_CONFIG_DIR/sats.list" | cut -d, -f3`
TLE="$REDSAT_CONFIG_DIR/elements/$SAT.txt"
TLEALL=`cat "$TLE" | paste -sd "," -`

META=${REDSAT_INPUT_DIR}/${OUTPUT_BASE}.meta
cat > $META <<-EOF
[main]
creation_time=$OUTPUT_BASE
samp_rate=$SDRSAMP
freq=$FREQ
gain=$SDRGAIN
time=$OUTPUT_BASE
[tle]
tle=$TLEALL
[position]
lat=$LAT
lon=$LON
elv=$ELV
EOF

python /app/gr/wav_to_raw.py --meta-input-file=/app/import/$INPUT --meta-output-file=/app/input/$OUTPUT_BASE.raw --meta-samp-rate=$SDRSAMP