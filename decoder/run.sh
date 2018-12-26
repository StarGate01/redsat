#!/bin/bash

source /app/TLE/station.config

KIND=$1
INPUT_BASE=$2
OUTPUT=${INPUT_BASE}_$(date +%s)

mkdir -p /app/output/$KIND/$OUTPUT
python /app/gr/$KIND.py --meta_input_file=/app/input/$INPUT_BASE.raw --meta_output_dir=/app/output/$KIND/$OUTPUT/ > /app/output/$KIND/$OUTPUT/decode.log