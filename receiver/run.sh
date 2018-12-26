#!/bin/bash

source /app/TLE/station.config

if [ -z "$1" ]; then
    SAT="MOVEII"
    echo "Warning: No satellite specified, defaulting to MOVE-II"
else
    SAT=$1
fi

if [ -z "$2" ]; then
    OUTPUT_BASE=`date +%s`
    echo "Warning: No output file specified, defaulting to current unix time stamp"
else
    OUTPUT_BASE=$2
fi

if [ -z "$3" ]; then
    KIND="receiver_nogui"
    echo "Warning: No gui flag specified, defaulting to No GUI"
else
    KIND="receiver"
fi

FREQ=`grep $SAT /app/TLE/sats.list | cut -d, -f3`
TLE="/app/TLE/elements/$SAT.txt"

META=/app/input/$OUTPUT_BASE.meta
echo `date +%s` >> $META
cat $TLE >> $META
echo $SDRSAMP >> $META
echo $FREQ >> $META
echo $LAT >> $META
echo $LON >> $META
echo $ELV >> $META

python /app/gr/$KIND.py --meta-output-file=/app/input/$OUTPUT_BASE.raw --meta-freq=$FREQ meta-gain=$SDRGAIN --meta-dev=$SDRDEV --meta-samp=$SDRSAMP

#gnuradio-companion /app/gr/receiver.grc