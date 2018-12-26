#!/bin/bash

FREQ=$1
LAT=$2
LON=$3
ELV=$4
TLE="/app/TLE/$5.txt"

TLELINES=$(cat $TLE | paste -sd "," -)
METAINFO="$SAMP;$FREQ;$TLELINES;$LAT;$LON;$ELV"

gnuradio-companion --meta_freq=$FREQ --meta_samp=$SAMP --meta_info="\"$METAINFO\""