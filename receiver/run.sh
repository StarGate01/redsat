#!/bin/bash

FREQ=$1
source /app/TLE/station.config

TLE="/app/TLE/elements/$2.txt"
TLELINES=$(cat $TLE | paste -sd "," -)
METAINFO="$SAMP;$FREQ;$TLELINES;$LAT;$LON;$ELV"

gnuradio-companion --meta_freq=$FREQ --meta_samp=$SAMP --meta_info="\"$METAINFO\""