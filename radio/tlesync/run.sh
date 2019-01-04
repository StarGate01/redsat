#!/bin/bash

rm -rf /app/config/elements
mkdir -p /app/config/elements
cd /app/config/elements && wget -i /app/config/sources.list -O all.tmp

while read p; do
    SAT=`echo $p | cut -d, -f1`
    FNAME=`echo $p | cut -d, -f2`
    sed -n "/$SAT\\s*$/{p;n;p;n;p;q}" /app/config/elements/all.tmp >> "/app/config/elements/$FNAME.txt"
    cat "/app/config/elements/$FNAME.txt"
done </app/config/sats.list

rm /app/config/elements/all.tmp