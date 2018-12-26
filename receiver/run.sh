#!/bin/bash

source /app/TLE/station.config

FREQ=$1
TLE="/app/TLE/elements/$2.txt"
OUTPUT_BASE=$3

TLELINES=$(cat $TLE | paste -sd "," -)
METAINFO="$SAMP;$FREQ;$TLELINES;$LAT;$LON;$ELV"

# python /app/gr/receive.py 
gnuradio-companion --meta_output_file=/app/output/$OUTPUT_BASE.raw --meta_freq=$FREQ --meta_dev=$SDRDEV --meta_samp=$SDRSAMP --meta_info="\"$METAINFO\""